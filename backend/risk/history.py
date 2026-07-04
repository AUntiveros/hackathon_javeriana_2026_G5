"""Ajuste bayesiano simple (Beta-Bernoulli) de los priors del motor de riesgo global,
usando el historial de Actividad ya almacenado. Sin ML entrenado, sin Event nuevos:
el conteo de incumplimientos pasados de un tipo de actividad ES el historial.
"""
from datetime import date, timedelta

from sqlmodel import select

from backend.db.models import Actividad, get_session


def tasa_historica(patient_id: int, tipo: str, dias: int = 7) -> float:
    """Tasa Beta-Bernoulli (prior Beta(1,1)) de incumplimiento histórico de `tipo` de
    actividad en los últimos `dias` (excluye hoy). Sin historial -> 0.5 (prior neutro,
    ni bajo ni alto)."""
    hoy = date.today()
    desde = (hoy - timedelta(days=dias)).isoformat()
    hasta = (hoy - timedelta(days=1)).isoformat()
    with get_session() as s:
        acts = s.exec(
            select(Actividad).where(
                Actividad.patient_id == patient_id,
                Actividad.tipo == tipo,
                Actividad.fecha >= desde,
                Actividad.fecha <= hasta,
            )
        ).all()
    total = len(acts)
    incumplidas = sum(1 for a in acts if a.estado != "confirmada" or a.n_rechazos > 0)
    return (incumplidas + 1) / (total + 2)
