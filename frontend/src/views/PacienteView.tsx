import { useCallback, useRef, useState } from 'react';
import Nino, { type NinoMood } from '../components/Nino/Nino';
import { chat, PATIENT_ID } from '../api/client';
import { useVoz } from '../hooks/useVoz';
import './paciente.css';

type Fase = 'reposo' | 'escuchando' | 'pensando' | 'hablando';

/**
 * F2 — Vista Paciente: chat de voz con Nino.
 * Botón hablar → STT es-PE → POST /chat → TTS + animación.
 * Sin STT (iOS viejo, Firefox): campo de texto grande como fallback.
 */
export default function PacienteView() {
  const [fase, setFase] = useState<Fase>('reposo');
  const [mood, setMood] = useState<NinoMood>('idle');
  const [burbuja, setBurbuja] = useState('¡Hola Don José! Toque el botón y conversamos.');
  const [dicho, setDicho] = useState(''); // lo que dijo el paciente
  const [textoManual, setTextoManual] = useState('');
  const ocupadoRef = useRef(false);
  const voz = useVoz();

  const conversar = useCallback(
    async (mensajeEscrito?: string) => {
      if (ocupadoRef.current) return;
      ocupadoRef.current = true;

      let mensaje = mensajeEscrito ?? '';

      // 1) escuchar (STT real)
      if (!mensajeEscrito && voz.sttSoportado) {
        setFase('escuchando');
        setMood('listening');
        setBurbuja('Lo escucho…');
        setDicho('');
        mensaje = await voz.escuchar();
        if (!mensaje) {
          setBurbuja('No le escuché bien. ¿Me lo repite, por favor?');
          setFase('reposo');
          setMood('idle');
          ocupadoRef.current = false;
          return;
        }
        setDicho(mensaje);
      }

      // 2) pensar (orquestador)
      setFase('pensando');
      setMood('thinking');
      setBurbuja('Mmm, déjame pensar…');
      const res = await chat({ rol: 'paciente', mensaje, patient_id: PATIENT_ID });

      // 3) responder
      const moodRespuesta: NinoMood =
        res.emocion === 'feliz' ? 'happy' : res.emocion === 'preocupado' ? 'concerned' : 'idle';
      setFase('hablando');
      setMood(moodRespuesta);
      setBurbuja(res.respuesta);
      voz.hablar(res.respuesta, () => {
        setFase('reposo');
        setMood('idle');
        ocupadoRef.current = false;
      });
    },
    [voz],
  );

  const enviarTexto = () => {
    const t = textoManual.trim();
    if (!t) return;
    setDicho(t);
    setTextoManual('');
    void conversar(t);
  };

  const speaking = fase === 'hablando';

  return (
    <div className="paciente">
      <section className="paciente__escenario" aria-live="polite">
        <div className="paciente__burbuja">{burbuja}</div>
        <Nino mood={mood} speaking={speaking} size="min(64vw, 300px)" />
        {dicho && (
          <p className="paciente__dicho">
            Usted dijo: <strong>“{dicho}”</strong>
          </p>
        )}
      </section>

      <button
        className="paciente__hablar"
        onClick={() => void conversar()}
        disabled={fase !== 'reposo'}
      >
        {fase === 'reposo' && '🎤 Hablar con Nino'}
        {fase === 'escuchando' && '👂 Lo escucho…'}
        {fase === 'pensando' && 'Pensando…'}
        {fase === 'hablando' && 'Nino responde…'}
      </button>

      {!voz.sttSoportado && (
        <div className="paciente__fallback">
          <label htmlFor="msj">Su navegador no tiene micrófono de voz. Escríbale a Nino:</label>
          <div className="paciente__fila">
            <input
              id="msj"
              value={textoManual}
              onChange={(e) => setTextoManual(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && enviarTexto()}
              placeholder="Hola Nino…"
            />
            <button onClick={enviarTexto} disabled={fase !== 'reposo'}>
              Enviar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
