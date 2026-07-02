/**
 * Cliente API — punto único de integración con el backend.
 * Si VITE_API_URL está definida usa el backend real (FastAPI);
 * si no, cae al mock. Las vistas importan SOLO de este archivo.
 */

import * as mock from './mock';
import type {
  Alerta,
  ChatRequest,
  ChatResponse,
  RoutineEvent,
  SenalClinica,
  Snapshot,
  TrendPoint,
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

export const PATIENT_ID = 1; // Don José — único paciente de la demo
