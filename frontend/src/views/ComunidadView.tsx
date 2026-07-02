import { useState } from 'react';
import './comunidad.css';

interface Par {
  id: number;
  nombre: string;
  edad: number;
  intereses: string[];
  afinidad: number; // %
}

/** Matching por intereses (scope RBAC: sin datos sensibles del paciente). */
const PARES: Par[] = [
  { id: 1, nombre: 'Don Ernesto', edad: 81, intereses: ['agricultura', 'ajedrez'], afinidad: 92 },
  { id: 2, nombre: 'Doña Carmen', edad: 76, intereses: ['música criolla', 'cocina'], afinidad: 87 },
  { id: 3, nombre: 'Don Aurelio', edad: 79, intereses: ['fútbol', 'huerto'], afinidad: 74 },
];

/** F4 — Vista Comunidad: conectar pares con intereses comunes. */
export default function ComunidadView() {
  const [invitados, setInvitados] = useState<number[]>([]);

  const invitar = (id: number) => setInvitados((prev) => [...prev, id]);

  return (
    <div className="vista">
      <section className="tarjeta">
        <h2>Vecinos con intereses en común</h2>
        <p className="comunidad__sub">Club del adulto mayor — San Juan de Miraflores</p>
        <ul className="comunidad__pares">
          {PARES.map((p) => (
            <li key={p.id} className="comunidad__par">
              <div className="comunidad__info">
                <strong>{p.nombre} · {p.edad}</strong>
                <small>{p.intereses.join(' · ')}</small>
                <span className="comunidad__afinidad">{p.afinidad}% afinidad con Don José</span>
              </div>
              {invitados.includes(p.id) ? (
                <span className="comunidad__ok">✓ Invitado</span>
              ) : (
                <button className="comunidad__boton" onClick={() => invitar(p.id)}>
                  Invitar
                </button>
              )}
            </li>
          ))}
        </ul>
      </section>

      <section className="tarjeta">
        <h2>📅 Próximo encuentro</h2>
        <p className="comunidad__evento">
          <strong>Tarde de música criolla</strong> — sábado 4 pm, local comunal.
          <br />
          Don José y 5 vecinos confirmados.
        </p>
      </section>
    </div>
  );
}
