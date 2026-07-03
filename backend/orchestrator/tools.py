"""Herramientas (tools) que los agentes de rol pueden invocar.

Alineadas al foco de rutina: consultar la memoria del paciente, la rutina, adherencia y vitales.
Nada cognitivo/diagnóstico.
"""
from sqlmodel import select

from backend.db.models import Actividad, Patient, Vital, get_session
from backend.routine import engine as routine

try:
    from backend.rag.retriever import query as pkg_query
except Exception:
    pkg_query = None


def consultar_pkg(texto: str, k: int = 3) -> list[str]:
    """Recupera memoria del paciente (personas, lugares, gustos, indicaciones)."""
    if pkg_query is None:
        return ["(PKG no disponible: corre `python -m backend.rag.ingest`)"]
    try:
        return pkg_query(texto, k)
    except Exception:
        return ["(PKG aún no ingestado: corre `python -m backend.rag.ingest`)"]


def rutina_hoy(patient_id: int) -> dict:
    """Actividades programadas de hoy y su estado."""
    return routine.plan_dia(patient_id)


def reporte_adherencia(patient_id: int) -> dict:
    """Resumen NO cognitivo: adherencia a rutina + últimos vitales (para el médico/cuidador)."""
    rep = routine.reporte_adherencia(patient_id)
    with get_session() as s:
        v = s.exec(select(Vital).where(Vital.patient_id == patient_id)
                   .order_by(Vital.timestamp.desc())).first()
    if v:
        rep["ultimo_vital"] = {"hr": v.hr, "bp_sys_est": v.bp_sys_est, "bp_dia_est": v.bp_dia_est}
    return rep


def sugerir_contacto(patient_id: int) -> dict:
    """Sugiere con quién conectar y prepara contexto desde el PKG."""
    ctx = consultar_pkg("familia nieta hija llamada reminiscencia", k=2)
    return {"sugerencia": "Buen momento para una llamada familiar", "contexto_conversacion": ctx}


def get_patient(patient_id: int) -> Patient | None:
    with get_session() as s:
        return s.exec(select(Patient).where(Patient.id == patient_id)).first()
