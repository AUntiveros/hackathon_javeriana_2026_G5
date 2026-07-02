"""Motor de rutina — orquestación del día a día del paciente (diagrama spec §5).

Genera la agenda del día con: check-in, medicación, actividad NO repetitiva, monitoreo,
conexión humana, cierre. Incluye escalado de alertas al cuidador.
"""
from datetime import datetime, timedelta

from sqlmodel import select

from backend.db.models import Biomarker, Event, get_session
from backend.orchestrator import tools

# Catálogo de actividades no repetitivas (rotación anti-aburrimiento)
_ACTIVIDADES = [
    "ver fotos de la boda y conversar (reminiscencia)",
    "escuchar y cantar música criolla",
    "hablar del partido de Cienciano 2003",
    "describir una foto de la chacra (ejercita lenguaje)",
    "juego de las veinte preguntas (atención)",
    "contar cómo conoció a María (memoria autobiográfica)",
    "orientación: qué día es hoy y qué haremos",
]


def elegir_actividad(patient_id: int) -> str:
    """Elige una actividad evitando repetir las últimas usadas."""
    with get_session() as s:
        recientes = s.exec(
            select(Event)
            .where(Event.patient_id == patient_id, Event.tipo == "actividad")
            .order_by(Event.timestamp.desc())
        ).all()
    usadas = {e.payload.get("actividad") for e in recientes[:4]}
    for act in _ACTIVIDADES:
        if act not in usadas:
            return act
    return _ACTIVIDADES[0]


def _riesgo_actual(patient_id: int) -> float:
    with get_session() as s:
        b = s.exec(
            select(Biomarker)
            .where(Biomarker.patient_id == patient_id)
            .order_by(Biomarker.timestamp.desc())
        ).first()
    return b.riesgo_score if b else 0.0


def plan_dia(patient_id: int = 1) -> dict:
    patient = tools.get_patient(patient_id)
    if not patient:
        return {"error": "paciente no encontrado"}

    med = next(iter(patient.rutina_base.values()), "medicación")
    actividad = elegir_actividad(patient_id)
    riesgo = _riesgo_actual(patient_id)

    agenda = [
        {"hora": "08:00", "tipo": "check-in", "detalle": "Saludo + orientación temporal + '¿cómo durmió?'"},
        {"hora": "08:30", "tipo": "medicacion", "detalle": "Recordatorio de pastilla azul (donepezilo) + vibración wearable"},
        {"hora": "10:00", "tipo": "actividad", "detalle": actividad},
        {"hora": "13:00", "tipo": "monitoreo", "detalle": "FC/pasos del wearable → Gemelo Cognitivo"},
        {"hora": "18:00", "tipo": "conexion", "detalle": "Sugerir llamada a la nieta Sofía (último tema: cumpleaños del bisnieto)"},
        {"hora": "20:00", "tipo": "cierre", "detalle": "Consolidar día: adherencia, ánimo, léxico"},
    ]

    alertas = []
    if riesgo > 0.55:
        alertas.append(
            {
                "nivel": "medio",
                "mensaje": f"Riesgo del habla elevado ({riesgo}). Reforzar actividad cognitiva y avisar al médico en la próxima cita.",
            }
        )

    return {
        "patient_id": patient_id,
        "fecha": datetime.utcnow().date().isoformat(),
        "agenda": agenda,
        "actividad_elegida": actividad,
        "riesgo_actual": riesgo,
        "alertas": alertas,
    }
