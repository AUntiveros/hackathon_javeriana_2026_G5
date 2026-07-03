import PacienteApp from './apps/PacienteApp';
import EquipoApp from './apps/EquipoApp';
import './App.css';

/**
 * Dos apps, un deploy:
 *   /paciente → app del Paciente (pantalla única, PWA instalable, "oye Nino")
 *   /         → app del Equipo (cuidador, médico, familiar, comunidad)
 */
export default function App() {
  const esPaciente = window.location.pathname.startsWith('/paciente');
  return esPaciente ? <PacienteApp /> : <EquipoApp />;
}
