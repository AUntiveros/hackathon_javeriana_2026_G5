/**
 * Cliente API — punto único de integración con el backend.
 * Si VITE_API_URL está definida usa el backend real (FastAPI);
 * si no, cae al mock. Las vistas importan SOLO de este archivo.
 */

import * as mock from './mock';
import type {
  ActividadV2,
  Adherencia,
  Alerta,
  AlertaCuidador,
  ChatRequest,
  ChatResponse,
  DecisionCriticidad,
  RoutineEvent,
  SenalClinica,
  Snapshot,
  TrendPoint,
  VitalV2,
} from './types';

const API_URL: string | undefined = import.meta.env.VITE_API_URL;

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`);
  if (!res.ok) throw new Error(`GET ${path} → ${res.status}`);
  return res.json();
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST ${path} → ${res.status}`);
  return res.json();
}

export function chat(req: ChatRequest): Promise<ChatResponse> {
  return API_URL ? post('/chat', req) : mock.chat(req);
}

export function getRoutineToday(patientId: number): Promise<RoutineEvent[]> {
  return API_URL ? get(`/routine/${patientId}/today`) : mock.getRoutineToday(patientId);
}

export function logMedicacion(eventId: number): Promise<void> {
  return API_URL ? post(`/events/${eventId}/done`, {}) : mock.logMedicacion(eventId);
}

export function getTwinTrend(patientId: number): Promise<TrendPoint[]> {
  return API_URL ? get(`/twin/${patientId}/trend`) : mock.getTwinTrend(patientId);
}

export function getTwinAlerts(patientId: number): Promise<Alerta[]> {
  return API_URL ? get(`/twin/${patientId}/alerts`) : mock.getTwinAlerts(patientId);
}

export function getTwinSnapshot(patientId: number): Promise<Snapshot> {
  return API_URL ? get(`/twin/${patientId}/snapshot`) : mock.getTwinSnapshot(patientId);
}

export function getSenalesClinicas(patientId: number): Promise<SenalClinica[]> {
  return API_URL ? get(`/twin/${patientId}/signals`) : mock.getSenalesClinicas(patientId);
}

// ============================================================
// API v2 (post-pivote) — rutina, criticidad, alertas, adherencia, vitales.
// Requieren VITE_API_URL (backend real). El mock v2 se añade en mock.ts.
// ============================================================

export async function getActividadesHoy(patientId: number): Promise<{ actividades: ActividadV2[] }> {
  return get(`/routine/${patientId}/today`);
}

export function procesarRutina(patientId: number, receptividad = 0.6): Promise<{ recordatorios: DecisionCriticidad[] }> {
  return post(`/routine/${patientId}/procesar`, { receptividad });
}

export function evaluarActividad(actId: number, receptividad = 0.6): Promise<DecisionCriticidad> {
  return get(`/actividades/${actId}/evaluar?receptividad=${receptividad}`);
}

export function confirmarActividad(actId: number): Promise<unknown> {
  return post(`/actividades/${actId}/confirmar`, {});
}

export function rechazarActividad(actId: number): Promise<unknown> {
  return post(`/actividades/${actId}/rechazar`, {});
}

export function getAlertas(patientId: number): Promise<AlertaCuidador[]> {
  return get(`/alertas/${patientId}`);
}

export function atenderAlerta(alertaId: number): Promise<unknown> {
  return post(`/alertas/${alertaId}/atender`, {});
}

export function getAdherencia(patientId: number): Promise<Adherencia> {
  return get(`/reporte/${patientId}/adherencia`);
}

export function postVital(patientId: number, hr: number, hrv_ms = 0): Promise<unknown> {
  return post('/vitals', { patient_id: patientId, hr, hrv_ms });
}

export function getVitals(patientId: number): Promise<VitalV2[]> {
  return get(`/vitals/${patientId}`);
}

export const PATIENT_ID = 1; // paciente único de la demo
