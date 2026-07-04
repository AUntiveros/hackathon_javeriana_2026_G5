import { useEffect, useState } from 'react';
import TwinDashboard from '../components/TwinDashboard/TwinDashboard';
import { getSenalesClinicas, PATIENT_ID } from '../api/client';
import type { SenalClinica } from '../api/types';
import './medico.css';

const FLECHA = { sube: '▲', baja: '▼', estable: '—' } as const;

/**
 * F4 — Vista Médico: señales clínicas derivadas del habla + tendencia
 * longitudinal + disclaimer obligatorio (spec §7). Tono técnico.
 */
export default function MedicoView() {
  const [senales, setSenales] = useState<SenalClinica[]>([]);

  useEffect(() => {
    void getSenalesClinicas(PATIENT_ID).then(setSenales);
  }, []);

  return (
    <div className="vista">
      <div className="disclaimer" role="note">
        ⚕️ Apoyo informativo derivado de sensado del habla. <strong>No constituye diagnóstico</strong>;
        la decisión clínica corresponde al profesional tratante.
      </div>

      <section className="tarjeta">
        <h2>Señales clínicas del habla</h2>
        <p className="medico__meta">Paciente: Don Manuel · 78a · M · escolaridad primaria (ajuste SES activo)</p>
        <div className="medico__tabla-wrap">
          <table className="medico__tabla">
            <thead>
              <tr>
                <th scope="col">Señal</th>
                <th scope="col">Cambio</th>
                <th scope="col">Relevancia</th>
              </tr>
            </thead>
            <tbody>
              {senales.map((s) => (
                <tr key={s.id}>
                  <td>{s.senal}</td>
                  <td className={`medico__dir medico__dir--${s.direccion}`}>
                    <span aria-hidden="true">{FLECHA[s.direccion]}</span> {s.cambio}
                  </td>
                  <td>
                    <span className={`medico__rel medico__rel--${s.relevancia}`}>{s.relevancia}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <TwinDashboard variante="completo" />
    </div>
  );
}
