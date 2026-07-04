import { useEffect, useRef, useState } from 'react';
import Tito, { type TitoMood } from '../components/Tito/Tito';
import { useAcompanante, type EstadoAcompanante } from '../hooks/useAcompanante';
import './paciente-app.css';

const MOOD_POR_ESTADO: Record<EstadoAcompanante, TitoMood> = {
  apagado: 'idle',
  dormido: 'sleeping',
  atento: 'listening',
  pensando: 'thinking',
  hablando: 'idle', // se ajusta con la emoción
};

/**
 * App del Paciente — una sola pantalla, cero menús.
 * Tito siempre presente: duerme, despierta con "Tito", conversa.
 * Instalable como PWA (fullscreen, ícono propio, pantalla encendida).
 */
export default function PacienteApp() {
  const n = useAcompanante();
  const [textoManual, setTextoManual] = useState('');
  const horaRef = useRef<HTMLParagraphElement>(null);

  // reloj grande: orientación temporal para el paciente
  useEffect(() => {
    const tick = () => {
      if (horaRef.current) {
        horaRef.current.textContent = new Date().toLocaleTimeString('es-PE', {
          hour: '2-digit',
          minute: '2-digit',
        });
      }
    };
    tick();
    const id = setInterval(tick, 10_000);
    return () => clearInterval(id);
  }, []);

  // manifest propio para instalar "Tito" como app independiente
  useEffect(() => {
    const link = document.querySelector<HTMLLinkElement>('link[rel="manifest"]');
    const anterior = link?.href ?? '';
    if (link) link.href = '/manifest-paciente.webmanifest';
    document.title = 'Tito — Mi compañero';
    return () => {
      if (link && anterior) link.href = anterior;
    };
  }, []);

  const mood: TitoMood =
    n.estado === 'hablando'
      ? n.emocion === 'feliz'
        ? 'happy'
        : n.emocion === 'preocupado'
          ? 'concerned'
          : 'idle'
      : MOOD_POR_ESTADO[n.estado];

  const fecha = new Date().toLocaleDateString('es-PE', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  });

  return (
    <main className={`papp papp--${n.estado}`}>
      <header className="papp__reloj">
        <p ref={horaRef} className="papp__hora" />
        <p className="papp__fecha">{fecha}</p>
      </header>

      <section className="papp__centro" aria-live="polite">
        {n.frase && <div className="papp__burbuja">{n.frase}</div>}
        <Tito mood={mood} speaking={n.estado === 'hablando'} size="min(70vw, 340px)" />
        {n.dicho && (
          <p className="papp__dicho">“{n.dicho}”</p>
        )}
      </section>

      {n.estado === 'apagado' ? (
        <button className="papp__encender" onClick={() => void n.iniciar()}>
          Encender a Tito
        </button>
      ) : !n.sttSoportado ? (
        <div className="papp__manual">
          <input
            value={textoManual}
            onChange={(e) => setTextoManual(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && textoManual.trim()) {
                n.hablarManual(textoManual.trim());
                setTextoManual('');
              }
            }}
            placeholder="Escríbale a Tito…"
            aria-label="Mensaje para Tito"
          />
          <button
            onClick={() => {
              if (textoManual.trim()) {
                n.hablarManual(textoManual.trim());
                setTextoManual('');
              }
            }}
          >
            Hablar
          </button>
        </div>
      ) : (
        <p className="papp__pista">
          {n.estado === 'dormido' && 'Diga “Tito” para despertarme'}
          {n.estado === 'atento' && 'Lo estoy escuchando'}
          {n.estado === 'pensando' && 'Un momentito…'}
          {n.estado === 'hablando' && ' '}
        </p>
      )}

      {n.error && <p className="papp__error">{n.error}</p>}

      {/* apagado discreto para el cuidador, no para el paciente */}
      {n.estado !== 'apagado' && (
        <button className="papp__apagar" onClick={n.apagar} aria-label="Apagar modo acompañante">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <path d="M12 3v8" />
            <path d="M6.5 6.5a8 8 0 1 0 11 0" />
          </svg>
        </button>
      )}
    </main>
  );
}
