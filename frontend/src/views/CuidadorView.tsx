import { useEffect, useState } from 'react';
import TwinDashboard from '../components/TwinDashboard/TwinDashboard';
import WearablePanel from '../components/WearablePanel/WearablePanel';
import { getRoutineToday, logMedicacion, PATIENT_ID } from '../api/client';
import type { RoutineEvent, TipoEvento } from '../api/types';
import './cuidador.css';

const ICONO: Record<TipoEvento, string> = {
  medicacion: '💊',
  actividad: '🎨',
  conversacion: '💬',
  alerta: '🔔',
  cita: '🏥',
  conexion: '📞',
};

/**
 * F4 — Vista Cuidador: agenda del día (motor de rutina T5),
 * log de medicación y alertas del gemelo.
 */
export default function CuidadorView() {
  const [agenda, setAgenda] = useState<RoutineEvent[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    void getRoutineToday(PATIENT_ID).then((a) => {
      setAgenda(a);
      setCargando(false);
    });
  }, []);

  const marcarHecho = async (id: number) => {
    setAgenda((prev) => prev.map((e) => (e.id === id ? { ...e, estado: 'hecho' } : e)));
    await logMedicacion(id);
  };

  return (
    <div className="vista">
      <section className="tarjeta">
        <h2>Agenda de hoy — Don Manuel</h2>
        {cargando && <p className="cargando">Cargando agenda…</p>}
        <ul className="agenda">
          {agenda.map((e) => (
            <li key={e.id} className={`agenda__item agenda__item--${e.estado}`}>
              <span className="agenda__hora">{e.hora}</span>
              <span className="agenda__icono" aria-hidden="true">{ICONO[e.tipo]}</span>
              <span className="agenda__cuerpo">
                <strong>{e.titulo}</strong>
                <small>{e.detalle}</small>
              </span>
              {e.estado === 'hecho' ? (
                <span className="agenda__hecho" aria-label="hecho">✓</span>
              ) : (
                <button className="agenda__boton" onClick={() => void marcarHecho(e.id)}>
                  Hecho
                </button>
              )}
            </li>
          ))}
        </ul>
      </section>

      <section className="tarjeta consejo">
        <h2>Consejo de hoy</h2>
        <p>
          Evita preguntarle <em>"¿te acuerdas?"</em>. Mejor cuéntale tú la anécdota y deja que él
          la complete — reduce frustración y estimula memoria episódica.
        </p>
      </section>

      <WearablePanel />

      <TwinDashboard variante="resumen" />
    </div>
  );
}
