"""Herramientas (tools) que los agentes de rol pueden invocar.

Cada tool lee/escribe la DB o el PKG. El router expone a cada rol solo las tools de su scope.
"""
from datetime import datetime

from sqlmodel import select

from backend.db.models import Biomarker, Event, Patient, TwinSnapshot, get_session

try:
    from backend.rag.retriever import query as pkg_query
except Exception:  # RAG no ingestado aún
    pkg_query = None


def consultar_pkg(texto: str, k: int = 3) -> list[str]:
    """Recupera memoria del paciente (personas, lugares, objetos, eventos)."""
    if pkg_query is None:
        return ["(PKG no disponible: corre `python -m backend.rag.ingest`)"]
    try:
        return pkg_query(texto, k)
    except Exception:
        return ["(PKG aún no ingestado: corre `python -m backend.rag.ingest`)"]


def log_medicacion(patient_id: int, medicamento: str, tomada: bool) -> dict:
    with get_session() as s:
        e = Event(
            patient_id=patient_id,
            tipo="medicacion",
            payload={"medicamento": medicamento, "tomada": tomada},
            estado="hecho" if tomada else "omitido",
        )
        s.add(e)
        s.commit()
        s.refresh(e)
    return {"ok": True, "event_id": e.id, "tomada": tomada}


def agendar_actividad(patient_id: int, actividad: str, hora: str) -> dict:
    with get_session() as s:
        e = Event(
            patient_id=patient_id,
            tipo="actividad",
            payload={"actividad": actividad, "hora": hora},
        )
        s.add(e)
        s.commit()
        s.refresh(e)
    return {"ok": True, "event_id": e.id}


def reporte_clinico(patient_id: int) -> dict:
    """Resumen de señales clínicas del habla — SOLO lee datos reales (anti-alucinación)."""
    with get_session() as s:
        bios = s.exec(
            select(Biomarker).where(Biomarker.patient_id == patient_id).order_by(Biomarker.timestamp)
        ).all()
        snap = s.exec(
            select(TwinSnapshot)
            .where(TwinSnapshot.patient_id == patient_id)
            .order_by(TwinSnapshot.timestamp.desc())
        ).first()

    if not bios:
        return {"error": "sin biomarcadores"}
    primero, ultimo = bios[0], bios[-1]

    def delta(campo):
        a = primero.features.get(campo)
        b = ultimo.features.get(campo)
        if a in (None, 0) or b is None:
            return None
        return round((b - a) / abs(a) * 100, 1)

    return {
        "ventana_dias": (ultimo.timestamp - primero.timestamp).days,
        "riesgo_actual": ultimo.riesgo_score,
        "delta_ttr_pct": delta("ttr"),
        "delta_pausa_ratio_pct": delta("pausa_ratio"),
        "delta_repeticion_preguntas_pct": delta("repeticion_preguntas"),
        "snapshot": snap.dict() if snap else None,
        "nota": "Señales derivadas del habla. No constituye diagnóstico.",
    }


def sugerir_contacto(patient_id: int) -> dict:
    """Sugiere con quién conectar y prepara contexto de conversación desde el PKG."""
    ctx = consultar_pkg("familia nieta hija llamada reminiscencia", k=2)
    return {
        "sugerencia": "Buen momento para una llamada familiar",
        "contexto_conversacion": ctx,
    }


def get_patient(patient_id: int) -> Patient | None:
    with get_session() as s:
        return s.exec(select(Patient).where(Patient.id == patient_id)).first()
