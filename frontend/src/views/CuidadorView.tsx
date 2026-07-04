import { useEffect, useState } from 'react';
import TwinDashboard from '../components/TwinDashboard/TwinDashboard';
import WearablePanel from '../components/WearablePanel/WearablePanel';
import { atenderAlerta, confirmarActividad, getActividadesHoy, getAlertas, PATIENT_ID } from '../api/client';
import type { ActividadV2, AlertaCuidador } from '../api/types';
import './cuidador.css';

const ICONO: Record<ActividadV2['tipo'], string> = {
  medicacion: '💊',
  comida: '🍽️',
  cita: '🏥',
  autocuidado: '🧼',
  hobby: '🎨',
  actividad: '🚶',
};

/**
 * Vista Cuidador: agenda del día (motor de rutina v2) + alertas del motor de criticidad.
 */
export default function CuidadorView() {
  const [agenda, setAgenda] = useState<ActividadV2[]>([]);
  const [alertas, setAlertas] = useState<AlertaCuidador[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    void Promise.all([getActividadesHoy(PATIENT_ID), getAlertas(PATIENT_ID)]).then(([act, al]) => {
      setAgenda(act.actividades);
      setAlertas(al);
      setCargando(false);
    });
    const id = window.setInterval(() => {
      void getAlertas(PATIENT_ID).then(setAlertas);
    }, 60_000);
    return () => window.clearInterval(id);
  }, []);

  const marcarHecho = async (id: number) => {
    setAgenda((prev) => prev.map((a) => (a.id === id ? { ...a, estado: 'confirmada' } : a)));
    await confirmarActividad(id);
  };

  const marcarAtendida = async (id: number) => {
    setAlertas((prev) => prev.map((a) => (a.id === id ? { ...a, atendida: true } : a)));
    await atenderAlerta(id);
  };

  const pendientes = alertas.filter((a) => !a.atendida);

  return (
    <div className="vista">
      {pendientes.length > 0 && (
        <section className="tarjeta alertas">
          <h2>Alertas</h2>
          <ul className="alertas__lista">
            {pendientes.map((a) => (
              <li key={a.id} className={`alertas__item alertas__item--${a.nivel}`}>
                <span className="alertas__motivo">{a.motivo}</span>
                <button className="alertas__boton" onClick={() => void marcarAtendida(a.id)}>
                  Atender
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="tarjeta">
        <h2>Agenda de hoy — Don Manuel</h2>
        {cargando && <p className="cargando">Cargando agenda…</p>}
        <ul className="agenda">
          {agenda.map((a) => (
            <li
              key={a.id}
              className={`agenda__item agenda__item--${a.estado === 'confirmada' ? 'hecho' : 'pendiente'}`}
            >
              <span className="agenda__hora">{a.hora}</span>
              <span className="agenda__icono" aria-hidden="true">{ICONO[a.tipo]}</span>
              <span className="agenda__cuerpo">
                <strong>{a.nombre}</strong>
                <small>{a.tipo} · criticidad {(a.criticidad * 100).toFixed(0)}%</small>
              </span>
              {a.estado === 'confirmada' ? (
                <span className="agenda__hecho" aria-label="hecho">✓</span>
              ) : (
                <button className="agenda__boton" onClick={() => void marcarHecho(a.id)}>
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
