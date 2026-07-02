import type { Rol } from '../api/types';
import './role-selector.css';

const ROLES: { id: Rol; label: string; icono: string }[] = [
  { id: 'paciente', label: 'Paciente', icono: '🧓' },
  { id: 'cuidador', label: 'Cuidador', icono: '🤝' },
  { id: 'medico', label: 'Médico', icono: '🩺' },
  { id: 'familiar', label: 'Familiar', icono: '👨‍👩‍👧' },
  { id: 'comunidad', label: 'Comunidad', icono: '🏘️' },
];

interface Props {
  rol: Rol;
  onCambio: (rol: Rol) => void;
}

/** Selector de los 5 roles RBAC — cambiar rol cambia vista, tono y datos. */
export default function RoleSelector({ rol, onCambio }: Props) {
  return (
    <nav className="roles" aria-label="Seleccionar rol">
      {ROLES.map((r) => (
        <button
          key={r.id}
          className={`roles__chip ${rol === r.id ? 'roles__chip--activo' : ''}`}
          aria-pressed={rol === r.id}
          onClick={() => onCambio(r.id)}
        >
          <span className="roles__icono" aria-hidden="true">{r.icono}</span>
          {r.label}
        </button>
      ))}
    </nav>
  );
}
