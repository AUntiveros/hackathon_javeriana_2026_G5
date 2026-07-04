import { useState } from 'react';
import RoleSelector from '../components/RoleSelector';
import CuidadorView from '../views/CuidadorView';
import MedicoView from '../views/MedicoView';
import FamiliarView from '../views/FamiliarView';
import type { Rol } from '../api/types';

const SUBTITULO: Partial<Record<Rol, string>> = {
  cuidador: 'Cuidador aumentado — Don Manuel',
  medico: 'Señales clínicas del habla — Don Manuel',
  familiar: 'Cómo está tu papá hoy',
};

/**
 * App del Equipo de cuidado: cuidador, médico, familiar.
 * La experiencia del paciente vive aparte en /paciente (cero menús).
 */
export default function EquipoApp() {
  const [rol, setRol] = useState<Rol>('cuidador');

  return (
    <main className="app">
      <header className="app__header">
        <h1>Tito · Equipo</h1>
        <p>{SUBTITULO[rol]}</p>
      </header>

      <RoleSelector rol={rol} onCambio={setRol} excluir={['paciente']} />

      {rol === 'cuidador' && <CuidadorView />}
      {rol === 'medico' && <MedicoView />}
      {rol === 'familiar' && <FamiliarView />}

      <a className="app__link-paciente" href="/paciente">
        Ver la app del paciente →
      </a>
    </main>
  );
}
