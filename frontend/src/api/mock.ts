import type {
  Alerta,
  ChatRequest,
  ChatResponse,
  Patient,
  Rol,
  RoutineEvent,
  SenalClinica,
  Snapshot,
  TrendPoint,
} from './types';

/* ============================================================
   Datos semilla de "Don Manuel" — coherentes con backend/seed (T2):
   78 años, ex-agricultor, escolaridad primaria, quechua-español,
   hija Rosa, nieta Sofía. 30 días de tendencia leve de deterioro.
   ============================================================ */

export const DON_MANUEL: Patient = {
  id: 1,
  nombre: 'Don Manuel',
  edad: 78,
  sexo: 'M',
};

// ---------- chat por rol ----------

const RESPUESTAS_POR_ROL: Record<Rol, ChatResponse[]> = {
  paciente: [
    { respuesta: '¡Hola Don Manuel! Qué gusto escucharlo. ¿Cómo amaneció hoy?', emocion: 'feliz' },
    {
      respuesta: 'Hoy toca su pastilla de las 9. Ya le aviso a Rosa que usted está muy bien.',
      emocion: 'neutral',
      tools_usadas: ['log_medicacion'],
    },
    {
      respuesta: '¿Le gustaría que pongamos un valsecito criollo mientras conversamos de su chacra?',
      emocion: 'feliz',
    },
    {
      respuesta: 'Lo noto un poquito cansado. ¿Quiere que llamemos a Sofía? Ella siempre lo alegra.',
      emocion: 'preocupado',
      tools_usadas: ['sugerir_contacto'],
    },
  ],
  cuidador: [
    {
      respuesta:
        'Don Manuel durmió bien y ya desayunó. Pendiente: pastilla de las 9 (donepezilo 10 mg). Sugerencia: hoy evita preguntarle "¿te acuerdas?"; mejor cuéntale tú la anécdota y deja que él la complete.',
      emocion: 'neutral',
    },
    {
      respuesta:
        'Registrado. Esta semana la adherencia va en 86%. Si notas que repite la misma pregunta más de 3 veces en una hora, anótalo con el botón de alerta.',
      emocion: 'neutral',
      tools_usadas: ['log_medicacion'],
    },
  ],
  medico: [
    {
      respuesta:
        'Resumen de señales del habla (últimas 3 semanas): repetición de preguntas +25%, TTR −8%, pausas intra-oración +14%. Tendencia de riesgo: leve al alza (0.42 → 0.51). Adherencia farmacológica: 86%.\n\n⚕️ Este resumen es apoyo informativo derivado de sensado del habla; no constituye diagnóstico. La decisión clínica corresponde al profesional tratante.',
      emocion: 'neutral',
      tools_usadas: ['reporte_clinico'],
    },
  ],
  familiar: [
    {
      respuesta:
        'Tu papá está estable y de buen ánimo 😊. Hoy habló de su chacra y de música criolla. Buen momento para llamarlo: 4-6 pm. Tema que le encanta: el mundial del 70 y los valses de Chabuca.',
      emocion: 'feliz',
      tools_usadas: ['sugerir_contacto'],
    },
  ],
};

const turnos: Record<Rol, number> = {
  paciente: 0,
  cuidador: 0,
  medico: 0,
  familiar: 0,
};

/** Simula POST /chat con latencia del orquestador. */
export async function chat(req: ChatRequest): Promise<ChatResponse> {
  await delay(1200 + Math.random() * 800);
  const lista = RESPUESTAS_POR_ROL[req.rol];
  const r = lista[turnos[req.rol] % lista.length];
  turnos[req.rol] += 1;
  return r;
}

// ---------- GET /routine/1/today ----------

const RUTINA_HOY: RoutineEvent[] = [
  { id: 1, hora: '08:00', tipo: 'conversacion', titulo: 'Check-in de voz', detalle: 'Tito saluda y conversa 5 min (extrae biomarcadores)', estado: 'hecho' },
  { id: 2, hora: '09:00', tipo: 'medicacion', titulo: 'Donepezilo 10 mg', detalle: 'Con el desayuno, vaso de agua completo', estado: 'pendiente' },
  { id: 3, hora: '10:30', tipo: 'actividad', titulo: 'Reminiscencia musical', detalle: 'Valses de Chabuca Granda — no repetida en 5 días', estado: 'pendiente' },
  { id: 4, hora: '13:00', tipo: 'medicacion', titulo: 'Memantina 10 mg', detalle: 'Con el almuerzo', estado: 'pendiente' },
  { id: 5, hora: '16:30', tipo: 'conexion', titulo: 'Llamada con Sofía', detalle: 'Su nieta — punto de conexión humana del día', estado: 'pendiente' },
  { id: 6, hora: '19:00', tipo: 'conversacion', titulo: 'Cierre del día', detalle: 'Conversación tranquila + revisión de mañana', estado: 'pendiente' },
];

export async function getRoutineToday(patientId: number): Promise<RoutineEvent[]> {
  void patientId;
  await delay(300);
  return structuredClone(RUTINA_HOY);
}

/** Simula tool log_medicacion: marca evento como hecho. */
export async function logMedicacion(eventId: number): Promise<void> {
  await delay(250);
  const ev = RUTINA_HOY.find((e) => e.id === eventId);
  if (ev) ev.estado = 'hecho';
}

// ---------- GET /twin/1/trend — 30 días, deterioro leve ----------

function generarTendencia(): TrendPoint[] {
  const puntos: TrendPoint[] = [];
  const hoy = new Date('2026-07-02');
  for (let i = 29; i >= 0; i--) {
    const d = new Date(hoy);
    d.setDate(hoy.getDate() - i);
    const t = (29 - i) / 29; // 0 → 1 a lo largo del mes
    const ruido = () => (Math.sin(i * 3.7) + Math.cos(i * 1.3)) * 2.2;
    // riesgo con ondulación semanal suave (buenos y malos días, sin serrucho)
    const onda = Math.sin(((29 - i) / 7) * Math.PI) * 0.012;
    puntos.push({
      fecha: d.toISOString().slice(0, 10),
      riesgo: +(0.42 + t * 0.09 + onda + ruido() / 400).toFixed(3),
      fluidez: +(72 - t * 7 + ruido()).toFixed(1),
      riqueza_lexica: +(68 - t * 6 + ruido()).toFixed(1),
      pausas: +(31 + t * 9 + ruido()).toFixed(1),
    });
  }
  return puntos;
}

const TENDENCIA = generarTendencia();

export async function getTwinTrend(patientId: number): Promise<TrendPoint[]> {
  void patientId;
  await delay(400);
  return TENDENCIA;
}

// ---------- GET /twin/1/alerts ----------

const ALERTAS: Alerta[] = [
  {
    id: 1,
    fecha: '2026-07-01',
    severidad: 'media',
    titulo: 'Repetición de preguntas al alza',
    detalle: '+25% en 3 semanas. Sugerencia: informar al médico en el próximo control.',
  },
  {
    id: 2,
    fecha: '2026-06-29',
    severidad: 'info',
    titulo: 'Buen día cognitivo',
    detalle: 'Fluidez y ánimo por encima de su promedio tras la llamada con Sofía.',
  },
  {
    id: 3,
    fecha: '2026-06-27',
    severidad: 'alta',
    titulo: 'Medicación omitida',
    detalle: 'Memantina de las 13:00 no registrada. Se notificó a Rosa (cuidadora).',
  },
];

export async function getTwinAlerts(patientId: number): Promise<Alerta[]> {
  void patientId;
  await delay(350);
  return ALERTAS;
}

// ---------- GET /twin/1/snapshot ----------

export async function getTwinSnapshot(patientId: number): Promise<Snapshot> {
  void patientId;
  await delay(300);
  return {
    estado_cognitivo: { valor: 64, etiqueta: 'Estable con señales leves' },
    estado_emocional: { valor: 78, etiqueta: 'Buen ánimo' },
    adherencia: { valor: 86, etiqueta: '86% esta semana' },
    riesgo: { valor: 51, etiqueta: 'Leve al alza' },
  };
}

// ---------- señales clínicas (vista médico, Capa B) ----------

const SENALES: SenalClinica[] = [
  { id: 1, senal: 'Repetición de preguntas', cambio: '+25% en 3 semanas', direccion: 'sube', relevancia: 'alta' },
  { id: 2, senal: 'Riqueza léxica (TTR)', cambio: '−8% en 30 días', direccion: 'baja', relevancia: 'alta' },
  { id: 3, senal: 'Pausas intra-oración', cambio: '+14% en 30 días', direccion: 'sube', relevancia: 'media' },
  { id: 4, senal: 'F0 (prosodia)', cambio: 'sin cambio significativo', direccion: 'estable', relevancia: 'baja' },
  { id: 5, senal: 'Velocidad del habla', cambio: '−5% en 30 días', direccion: 'baja', relevancia: 'media' },
];

export async function getSenalesClinicas(patientId: number): Promise<SenalClinica[]> {
  void patientId;
  await delay(350);
  return SENALES;
}

function delay(ms: number) {
  return new Promise((res) => setTimeout(res, ms));
}
