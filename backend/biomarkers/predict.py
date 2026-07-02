"""Predicción de riesgo desde features + ajuste de equidad SES.

Carga `ml/model.pkl` (de la terminal ML) si existe; si no, usa una heurística simulada para no
bloquear la demo. Siempre pasa por el SES personalizer (equidad).
"""
import pickle
from datetime import datetime
from pathlib import Path

from backend.db.models import Biomarker, get_session
from backend.ses import personalizer

MODEL_PATH = Path(__file__).resolve().parents[2] / "ml" / "model.pkl"

_model = None


def _load_model():
    global _model
    if _model is None and MODEL_PATH.exists():
        try:
            with open(MODEL_PATH, "rb") as f:
                _model = pickle.load(f)
        except Exception:
            _model = None
    return _model


def _riesgo_bruto(features: dict) -> float:
    model = _load_model()
    if model is not None:
        try:
            import numpy as np

            x = np.array([[v for v in features.values()]])
            proba = model.predict_proba(x)[0][-1]
            return float(proba)
        except Exception:
            pass
    # Heurística simulada: más pausas + menos TTR + más repetición => más riesgo
    ttr = features.get("ttr", 0.55)
    pausa = features.get("pausa_ratio", 0.2)
    rep = features.get("repeticion_preguntas", 3)
    r = 0.5 + (0.25 - pausa) * -1.2 + (0.55 - ttr) * 1.5 + (rep - 3) * 0.03
    return max(0.0, min(1.0, r))


def analizar(patient_id: int, features: dict, ses_metadata: dict, guardar: bool = True) -> dict:
    bruto = _riesgo_bruto(features)
    ajuste = personalizer.ajustar_riesgo(bruto, ses_metadata)
    version = "model.pkl" if MODEL_PATH.exists() else "heuristica-stub"

    if guardar:
        with get_session() as s:
            s.add(
                Biomarker(
                    patient_id=patient_id,
                    timestamp=datetime.utcnow(),
                    categoria="mixto",
                    features=features,
                    riesgo_score=ajuste["riesgo_ajustado"],
                    modelo_version=version,
                )
            )
            s.commit()

    return {"features": features, "modelo_version": version, **ajuste}
