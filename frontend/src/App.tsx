import { useState } from 'react';
import RoleSelector from './components/RoleSelector';
import PacienteView from './views/PacienteView';
import CuidadorView from './views/CuidadorView';
import MedicoView from './views/MedicoView';
import FamiliarView from './views/FamiliarView';
import ComunidadView from './views/ComunidadView';
import type { Rol } from './api/types';
import './App.css';

const SUBTITULO: Record<Rol, string> = {
  paciente: 'Tu compañero de cada día',
  cuidador: 'Cuidador aumentado — Don José',
  medico: 'Señales clínicas del habla — Don José',
  familiar: 'Cómo está tu papá hoy',
  comunidad: 'Red de pares — club de adulto mayor',
};

export default function App() {
  const [rol, setRol] = useState<Rol>('paciente');

  return (
    <main className="app">
      <header className="app__header">
        <h1>Nino</h1>
        <p>{SUBTITULO[rol]}</p>
      </header>

      <RoleSelector rol={rol} onCambio={setRol} />

      {rol === 'paciente' && <PacienteView />}
      {rol === 'cuidador' && <CuidadorView />}
      {rol === 'medico' && <MedicoView />}
      {rol === 'familiar' && <FamiliarView />}
      {rol === 'comunidad' && <ComunidadView />}
    </main>
  );
}
