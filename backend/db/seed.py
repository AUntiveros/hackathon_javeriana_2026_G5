"""Puebla la DB con Don José + 30 días de biomarcadores simulados con tendencia leve.

Uso:
    python -m backend.db.seed
"""
import json
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

from sqlmodel import select

from backend.db.models import (
    Biomarker,
    Event,
    Patient,
    TwinSnapshot,
    engine,
    get_session,
    init_db,
)

SEED_PATH = Path(__file__).resolve().parents[1] / "seed" / "don_jose.json"


def seed():
    init_db()
    data = json.loads(SEED_PATH.read_text(encoding="utf-8"))["patient"]

    with get_session() as s:
        if s.exec(select(Patient).where(Patient.id == 1)).first():
            print("[seed] ya existe Don José; nada que hacer")
            return

        p = Patient(
            id=1,
            nombre=data["nombre"],
            apodo=data["apodo"],
            edad=data["edad"],
            sexo=data["sexo"],
            diagnostico=data["diagnostico"],
            personalidad=data["personalidad"],
            ses_metadata=data["ses_metadata"],
            rutina_base=data["rutina_base"],
        )
        s.add(p)

        # 30 dias de biomarcadores con deterioro leve simulado (tendencia + ruido)
        base = datetime.utcnow() - timedelta(days=30)
        for d in range(30):
            t = base + timedelta(days=d)
            drift = d / 30.0  # 0 -> 1
            ttr = 0.62 - 0.08 * drift + random.uniform(-0.02, 0.02)
            pausa_ratio = 0.18 + 0.10 * drift + random.uniform(-0.015, 0.015)
            speech_rate = 3.4 - 0.5 * drift + random.uniform(-0.1, 0.1)
            riesgo = min(1.0, 0.25 + 0.4 * drift + random.uniform(-0.03, 0.03))
            s.add(
                Biomarker(
                    patient_id=1,
                    timestamp=t,
                    categoria="mixto",
                    features={
                        "ttr": round(ttr, 3),
                        "pausa_ratio": round(pausa_ratio, 3),
                        "speech_rate": round(speech_rate, 2),
                        "repeticion_preguntas": round(2 + 6 * drift, 1),
                    },
                    riesgo_score=round(riesgo, 3),
                    modelo_version="seed",
                )
            )
            if d % 5 == 0:
                s.add(
                    TwinSnapshot(
                        patient_id=1,
                        timestamp=t,
                        estado_cognitivo="leve" if drift < 0.6 else "leve-moderado",
                        estado_emocional="estable",
                        riesgo=round(riesgo, 3),
                        autonomia=round(1.0 - 0.3 * drift, 2),
                        adherencia=round(1.0 - 0.1 * random.random(), 2),
                        carga_cuidador=round(0.3 + 0.3 * drift, 2),
                    )
                )

        # un par de eventos de ejemplo
        s.add(Event(patient_id=1, tipo="cita", payload={"con": "neurólogo", "fecha": "2026-07-10"}))
        s.add(Event(patient_id=1, tipo="alerta", payload={"motivo": "sedentarismo prolongado"}, estado="pendiente"))
        s.commit()
    print("[seed] Don José + 30 días de biomarcadores cargados")


if __name__ == "__main__":
    seed()
