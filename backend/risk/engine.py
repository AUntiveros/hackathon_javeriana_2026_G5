"""Motor de riesgo global — capa cloud que combina varias actividades y vitales del
paciente en un P(Descompensacion) único vía red fuzzy-bayesiana, SIN reemplazar el
motor de criticidad por-actividad existente (backend/criticality/engine.py sigue
decidiendo insistencia individual, edge, sin cambios).
"""
from datetime import date, datetime, timedelta

from sqlmodel import select

from backend.db.models import Actividad, Alerta, Vital, get_session
from backend.risk import bayes_engine, evidence, history
from backend.routine.engine import _hoy, _retraso_min

PESO_HISTORIAL = 0.3  # cuanto pesa la tendencia historica frente a la señal de hoy

_TIERS = (
    (0.30, "ninguna"),
    (0.60, "preventivo"),
    (0.85, "agudo_moderado"),
    (1.01, "crisis"),
)


def _tier(p: float) -> str:
    for limite, nombre in _TIERS:
        if p < limite:
            return nombre
    return "crisis"


def _peor_retraso(acts: list[Actividad], tipo: str) -> float:
    candidatas = [a for a in acts if a.tipo == tipo]
    if not candidatas:
        return 0.0
    return max(_retraso_min(a.hora, a.ventana_min) for a in candidatas)


def _pasos_hoy_y_baseline(patient_id: int) -> tuple[int, int]:
    hoy = _hoy()
    desde = (date.today() - timedelta(days=7)).isoformat()
    with get_session() as s:
        vitals = s.exec(select(Vital).where(Vital.patient_id == patient_id)).all()
    de_hoy = [v for v in vitals if v.timestamp.date().isoformat() == hoy]
    pasados = [v for v in vitals if desde <= v.timestamp.date().isoformat() < hoy]
    pasos_hoy = max((v.pasos for v in de_hoy), default=0)
    por_dia: dict[str, int] = {}
    for v in pasados:
        dia = v.timestamp.date().isoformat()
        por_dia[dia] = max(por_dia.get(dia, 0), v.pasos)
    baseline = round(sum(por_dia.values()) / len(por_dia)) if por_dia else pasos_hoy
    return pasos_hoy, baseline


def _calcular_evidencias(patient_id: int) -> tuple[float, float, float]:
    hoy = _hoy()
    with get_session() as s:
        acts = s.exec(
            select(Actividad).where(Actividad.patient_id == patient_id, Actividad.fecha == hoy)
        ).all()

    retraso_med = _peor_retraso(acts, "medicacion")
    retraso_comida = _peor_retraso(acts, "comida")
    pasos_hoy, baseline = _pasos_hoy_y_baseline(patient_id)

    g_olvido = evidence.grado_olvido_medicacion(retraso_med)
    g_ayuno = evidence.grado_ayuno(retraso_comida)
    g_sedentarismo = evidence.grado_sedentarismo(pasos_hoy, baseline)

    hist_med = history.tasa_historica(patient_id, "medicacion")
    hist_comida = history.tasa_historica(patient_id, "comida")
    g_olvido = (1 - PESO_HISTORIAL) * g_olvido + PESO_HISTORIAL * hist_med
    g_ayuno = (1 - PESO_HISTORIAL) * g_ayuno + PESO_HISTORIAL * hist_comida

    return g_olvido, g_ayuno, g_sedentarismo


def _crear_alerta(patient_id: int, tier: str, p: float) -> None:
    """Crea (o actualiza) la alerta de riesgo global del paciente.

    Idempotente: si ya existe una alerta de riesgo global sin atender para este
    paciente, se actualiza in-place (nivel/motivo/timestamp) en vez de insertar
    una fila nueva — evita spam de alertas duplicadas si el endpoint se llama
    repetidamente (cron/polling) mientras el cuidador no atiende la anterior.
    """
    nivel = "alto" if tier in ("agudo_moderado", "crisis") else "medio"
    motivo = f"Riesgo global {tier}: P(descompensacion)={p:.2f}"
    with get_session() as s:
        existente = s.exec(
            select(Alerta).where(
                Alerta.patient_id == patient_id,
                Alerta.atendida == False,  # noqa: E712
                Alerta.motivo.startswith("Riesgo global "),
            )
        ).first()
        if existente:
            existente.nivel = nivel
            existente.motivo = motivo
            existente.timestamp = datetime.utcnow()
            s.add(existente)
        else:
            s.add(Alerta(patient_id=patient_id, nivel=nivel, motivo=motivo))
        s.commit()


def evaluar_riesgo_global(patient_id: int = 1) -> dict:
    g_olvido, g_ayuno, g_sedentarismo = _calcular_evidencias(patient_id)
    p = bayes_engine.inferir_riesgo(g_olvido, g_ayuno, g_sedentarismo)
    tier = _tier(p)

    if tier != "ninguna":
        _crear_alerta(patient_id, tier, p)

    return {
        "patient_id": patient_id,
        "p_descompensacion": round(p, 3),
        "tier": tier,
        "evidencias": {
            "olvido_medicacion": round(g_olvido, 3),
            "ayuno": round(g_ayuno, 3),
            "sedentarismo": round(g_sedentarismo, 3),
        },
    }
