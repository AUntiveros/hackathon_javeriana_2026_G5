"""Configuración del módulo Uno Q (visión + memoria + voz)."""
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent

# edge | cloud | auto  (auto = usa cloud si hay red, si no edge)
MODE = os.environ.get("UNOQ_MODE", "auto")

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
PATIENT_ID = int(os.environ.get("PATIENT_ID", "1"))

MODELS_DIR = BASE / "models"
DATA_DIR = BASE / "data"
DATA_DIR.mkdir(exist_ok=True)

OBJ_MODEL = MODELS_DIR / "coco_ssd_mobilenet.tflite"
OBJ_LABELS = MODELS_DIR / "labels.txt"
FACE_MODEL = DATA_DIR / "faces_lbph.yml"
FACE_LABELS = DATA_DIR / "faces_labels.json"
MYOBJECTS_STORE = DATA_DIR / "my_objects.json"
SPATIAL_DB = DATA_DIR / "spatial_memory.db"

DET_SCORE_MIN = float(os.environ.get("DET_SCORE_MIN", "0.5"))


def online() -> bool:
    """¿Hay red hacia el backend? Determina edge vs cloud en modo auto."""
    if MODE == "edge":
        return False
    if MODE == "cloud":
        return True
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=1).close()
        return True
    except Exception:
        return False
