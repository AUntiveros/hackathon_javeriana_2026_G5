import { useCallback, useEffect, useRef, useState } from 'react';
import { chat, PATIENT_ID } from '../api/client';

/**
 * Modo acompañante (app Paciente): Tito siempre presente.
 *
 * Máquina de estados:
 *   apagado → (botón) → dormido ⇄ atento → pensando → hablando → atento
 *                         ↑ wake word "Tito"          silencio 18s ↓
 *                         └──────────────────────────────────────────┘
 *
 * - dormido: micrófono abierto solo para la palabra clave ("Tito" / "oye Tito").
 * - atento: todo lo que diga el paciente va al orquestador.
 * - Mientras Tito habla, el micrófono se pausa (no se escucha a sí mismo).
 * - Wake Lock mantiene la pantalla encendida (teléfono en atril).
 *
 * Límite conocido: web no escucha con pantalla bloqueada/app cerrada.
 * El "oye Tito" desatendido de verdad va en la app nativa (Expo dev build
 * + Porcupine) y en el dispositivo de mesa — ver docs/plan.
 */

export type EstadoAcompanante = 'apagado' | 'dormido' | 'atento' | 'pensando' | 'hablando';

const WAKE_REGEX = /\b(oye\s+)?(tito)\b/i;
const SILENCIO_MS = 18_000;

const SpeechRecognitionImpl =
  typeof window !== 'undefined'
    ? (window.SpeechRecognition ?? window.webkitSpeechRecognition)
    : undefined;

export interface Acompanante {
  estado: EstadoAcompanante;
  frase: string; // lo que Tito dice / indicación en pantalla
  dicho: string; // último transcript del paciente
  emocion: 'neutral' | 'feliz' | 'preocupado';
  error: string | null;
  sttSoportado: boolean;
  iniciar: () => Promise<void>;
  apagar: () => void;
  /** fallback pulsar-para-hablar cuando no hay STT continuo */
  hablarManual: (texto: string) => void;
}

export function useAcompanante(): Acompanante {
  const [estado, setEstado] = useState<EstadoAcompanante>('apagado');
  const [frase, setFrase] = useState('');
  const [dicho, setDicho] = useState('');
  const [emocion, setEmocion] = useState<'neutral' | 'feliz' | 'preocupado'>('neutral');
  const [error, setError] = useState<string | null>(null);

  const estadoRef = useRef<EstadoAcompanante>('apagado');
  const recRef = useRef<SpeechRecognitionInstance | null>(null);
  const wakeLockRef = useRef<{ release: () => Promise<void> } | null>(null);
  const timerSilencioRef = useRef<number | null>(null);
  const vivoRef = useRef(false);

  const setEstadoTotal = useCallback((e: EstadoAcompanante) => {
    estadoRef.current = e;
    setEstado(e);
  }, []);

  // ---------- TTS ----------

  const hablar = useCallback(
    (texto: string, alTerminar: () => void) => {
      let fin = false;
      const done = () => {
        if (fin) return;
        fin = true;
        alTerminar();
      };
      setTimeout(done, Math.max(4000, texto.length * 90));
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(texto);
      u.lang = 'es-ES';
      u.rate = 0.92;
      u.pitch = 1.15;
      u.onend = done;
      u.onerror = done;
      window.speechSynthesis.speak(u);
    },
    [],
  );

  // ---------- silencio → volver a dormir ----------

  const armarTimerSilencio = useCallback(() => {
    if (timerSilencioRef.current) clearTimeout(timerSilencioRef.current);
    timerSilencioRef.current = window.setTimeout(() => {
      if (estadoRef.current === 'atento') {
        setEstadoTotal('dormido');
        setFrase('Estoy aquí. Diga “Tito” cuando me necesite.');
        setDicho('');
      }
    }, SILENCIO_MS);
  }, [setEstadoTotal]);

  // ---------- conversación ----------

  const conversar = useCallback(
    async (mensaje: string) => {
      detenerRec(recRef); // no escucharse a sí mismo
      if (timerSilencioRef.current) clearTimeout(timerSilencioRef.current);
      setDicho(mensaje);
      setEstadoTotal('pensando');
      setFrase('Mmm…');

      const res = await chat({ rol: 'paciente', mensaje, patient_id: PATIENT_ID });
      if (!vivoRef.current) return;

      setEmocion(res.emocion ?? 'neutral');
      setEstadoTotal('hablando');
      setFrase(res.respuesta);
      hablar(res.respuesta, () => {
        if (!vivoRef.current) return;
        setEstadoTotal('atento');
        setFrase('Lo escucho…');
        armarTimerSilencio();
        arrancarRec(); // reabrir micrófono
      });
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [hablar, armarTimerSilencio, setEstadoTotal],
  );

  // ---------- reconocimiento continuo ----------

  const arrancarRec = useCallback(() => {
    if (!SpeechRecognitionImpl || !vivoRef.current) return;
    detenerRec(recRef);

    const rec = new SpeechRecognitionImpl();
    recRef.current = rec;
    rec.lang = 'es-PE';
    rec.continuous = true;
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    rec.onresult = (e: SpeechRecognitionEvent) => {
      const r = e.results[e.results.length - 1];
      if (!r || !r.isFinal) return;
      const texto = r[0].transcript.trim();
      if (!texto) return;

      const est = estadoRef.current;
      if (est === 'dormido') {
        const m = WAKE_REGEX.exec(texto);
        if (!m) return; // ignora conversación ambiente
        const resto = texto.slice((m.index ?? 0) + m[0].length).trim();
        if (resto.length > 2) {
          void conversar(resto); // "Tito, ¿qué día es hoy?"
        } else {
          setEstadoTotal('atento');
          setFrase('¿Dígame, Don Manuel?');
          setDicho('');
          hablar('¿Dígame, Don Manuel?', () => {
            if (vivoRef.current && estadoRef.current === 'atento') armarTimerSilencio();
          });
        }
      } else if (est === 'atento') {
        void conversar(texto);
      }
    };

    rec.onend = () => {
      // Chrome corta solo; relanzar si seguimos en modo escucha
      const est = estadoRef.current;
      if (vivoRef.current && (est === 'dormido' || est === 'atento')) {
        setTimeout(() => {
          if (vivoRef.current && recRef.current === rec) arrancarRec();
        }, 250);
      }
    };

    rec.onerror = (e: Event) => {
      const err = (e as unknown as { error?: string }).error;
      if (err === 'not-allowed' || err === 'service-not-allowed') {
        setError('Permiso de micrófono denegado. Active el micrófono para hablar con Tito.');
        setEstadoTotal('apagado');
        vivoRef.current = false;
      }
      // otros errores (no-speech, network): onend relanza
    };

    try {
      rec.start();
    } catch {
      /* start() sobre rec ya activo: ignorar */
    }
  }, [conversar, hablar, armarTimerSilencio, setEstadoTotal]);

  // ---------- wake lock ----------

  const pedirWakeLock = useCallback(async () => {
    try {
      const nav = navigator as Navigator & {
        wakeLock?: { request: (t: 'screen') => Promise<{ release: () => Promise<void> }> };
      };
      if (nav.wakeLock) wakeLockRef.current = await nav.wakeLock.request('screen');
    } catch {
      /* sin wake lock: la pantalla puede apagarse, no es fatal */
    }
  }, []);

  useEffect(() => {
    const alVolver = () => {
      if (document.visibilityState === 'visible' && vivoRef.current) {
        void pedirWakeLock();
        arrancarRec();
      }
    };
    document.addEventListener('visibilitychange', alVolver);
    return () => document.removeEventListener('visibilitychange', alVolver);
  }, [pedirWakeLock, arrancarRec]);

  // ---------- API pública ----------

  const iniciar = useCallback(async () => {
    setError(null);
    vivoRef.current = true;
    await pedirWakeLock();

    if (!SpeechRecognitionImpl) {
      // sin STT: modo botón por turno (hablarManual)
      setEstadoTotal('atento');
      setFrase('Su navegador no escucha solo. Use el botón para hablar conmigo.');
      return;
    }

    setEstadoTotal('dormido');
    setFrase('Diga “Tito” y conversamos.');
    const saludo = '¡Hola Don Manuel! Aquí estoy, acompañándolo. Diga mi nombre, Tito, cuando quiera conversar.';
    setEstadoTotal('hablando');
    setFrase(saludo);
    setEmocion('feliz');
    hablar(saludo, () => {
      if (!vivoRef.current) return;
      setEstadoTotal('dormido');
      setFrase('Diga “Tito” y conversamos.');
      arrancarRec();
    });
  }, [hablar, arrancarRec, pedirWakeLock, setEstadoTotal]);

  const apagar = useCallback(() => {
    vivoRef.current = false;
    detenerRec(recRef);
    window.speechSynthesis?.cancel();
    if (timerSilencioRef.current) clearTimeout(timerSilencioRef.current);
    void wakeLockRef.current?.release().catch(() => {});
    wakeLockRef.current = null;
    setEstadoTotal('apagado');
    setFrase('');
    setDicho('');
  }, [setEstadoTotal]);

  const hablarManual = useCallback(
    (texto: string) => {
      if (estadoRef.current === 'pensando' || estadoRef.current === 'hablando') return;
      vivoRef.current = true;
      void conversar(texto);
    },
    [conversar],
  );

  useEffect(() => apagar, [apagar]); // cleanup al desmontar

  return {
    estado,
    frase,
    dicho,
    emocion,
    error,
    sttSoportado: Boolean(SpeechRecognitionImpl),
    iniciar,
    apagar,
    hablarManual,
  };
}

function detenerRec(ref: React.MutableRefObject<SpeechRecognitionInstance | null>) {
  const rec = ref.current;
  ref.current = null; // evita que onend lo relance
  try {
    rec?.abort();
  } catch {
    /* ya detenido */
  }
}
