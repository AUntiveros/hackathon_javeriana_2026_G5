/**
 * Contrato de API con el backend (FastAPI).
 * Fuente: docs/plan/implementation-plan.md (T4, T5, T8) y spec §5-6.
 * Hoy se consume vía mock (mock.ts); client.ts cambia a fetch real
 * usando VITE_API_URL sin tocar los componentes.
 */

/** Los 5 roles de la matriz RBAC (spec §6) */
export type Rol = 'paciente' | 'cuidador' | 'medico' | 'familiar' | 'comunidad';

// ---------- POST /chat ----------

export interface ChatRequest {
  rol: Rol;
  mensaje: string;
  patient_id: number;
}

export interface ChatResponse {
  respuesta: string;
  /** emoción sugerida por el orquestador para la mascota */
  emocion?: 'neutral' | 'feliz' | 'preocupado';
  /** herramientas ejecutadas por el agente (p.ej. log_medicacion) */
  tools_usadas?: string[];
}

// ---------- GET /patients/:id ----------

export interface Patient {
  id: number;
  nombre: string;
  edad: number;
  sexo: string;
  foto?: string;
}

// ---------- GET /routine/:id/today (T5) ----------

export type TipoEvento = 'medicacion' | 'actividad' | 'conversacion' | 'alerta' | 'cita' | 'conexion';

export interface RoutineEvent {
  id: number;
  hora: string; // "09:00"
  tipo: TipoEvento;
  titulo: string;
  detalle: string;
  estado: 'pendiente' | 'hecho' | 'omitido';
}

// ---------- GET /twin/:id/trend (T8) ----------

export interface TrendPoint {
  fecha: string; // ISO date
  /** score de riesgo 0-1 del clasificador */
  riesgo: number;
  /** métricas del habla normalizadas 0-100 para el dashboard */
  fluidez: number;
  riqueza_lexica: number;
  pausas: number;
}

// ---------- GET /twin/:id/alerts ----------

export interface Alerta {
  id: number;
  fecha: string;
  severidad: 'info' | 'media' | 'alta';
  titulo: string;
  detalle: string;
}

// ---------- GET /twin/:id/snapshot ----------

export interface Snapshot {
  estado_cognitivo: { valor: number; etiqueta: string };
  estado_emocional: { valor: number; etiqueta: string };
  adherencia: { valor: number; etiqueta: string };
  riesgo: { valor: number; etiqueta: string };
}

// ---------- Vista médico (Capa B mock) ----------

export interface SenalClinica {
  id: number;
  senal: string;
  cambio: string; // "+25% en 3 semanas"
  direccion: 'sube' | 'baja' | 'estable';
  relevancia: 'alta' | 'media' | 'baja';
}

// ---------- Wearable BLE (F5 / H1) ----------

export interface WearableData {
  fc: number; // frecuencia cardiaca bpm
  pasos: number;
  conectado: boolean;
}
