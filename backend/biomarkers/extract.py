"""Extracción de features del habla.

Contrato con la terminal ML: el orden/nombres de features deben coincidir con
`ml/feature_schema.json`. Mientras no estén librosa/whisper o falte audio, devuelve features
simuladas coherentes para no bloquear la integración del dashboard.
"""
import json
import random
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "ml" / "feature_schema.json"

# Features por defecto si aún no existe el schema del track ML (mantener sincronizado).
_DEFAULT_FEATURES = ["ttr", "pausa_ratio", "speech_rate", "repeticion_preguntas", "jitter", "shimmer"]


def _feature_names() -> list[str]:
    if SCHEMA_PATH.exists():
        try:
            return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))["features"]
        except Exception:
            pass
    return _DEFAULT_FEATURES


def extract(audio_path: str | None = None, transcript: str | None = None) -> dict:
    """Devuelve features del habla.

    Real (cuando estén las libs): Whisper→librosa/parselmouth/spaCy/webrtcvad.
    Stub (ahora): valores simulados dentro de rangos plausibles.
    """
    try:
        if audio_path:
            return _extract_real(audio_path, transcript)
    except Exception:
        pass  # cae al stub
    names = _feature_names()
    rng = {
        "ttr": (0.45, 0.65),
        "pausa_ratio": (0.15, 0.35),
        "speech_rate": (2.8, 3.6),
        "repeticion_preguntas": (1, 9),
        "jitter": (0.005, 0.03),
        "shimmer": (0.03, 0.09),
    }
    return {n: round(random.uniform(*rng.get(n, (0.0, 1.0))), 3) for n in names}


def _extract_real(audio_path: str, transcript: str | None) -> dict:
    """Pipeline real. Implementar cuando librosa/parselmouth/whisper estén instalados."""
    raise NotImplementedError("Pipeline real pendiente de libs (librosa/whisper/spaCy)")
