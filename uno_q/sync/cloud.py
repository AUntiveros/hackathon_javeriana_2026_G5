"""Sincronización de eventos de visión con el backend (alimenta el Gemelo/PKG del asistente).

Online: POST a /vision/ingest. Offline: encola en JSONL local y reintenta al reconectar.
Así la database del asistente se alimenta del entorno que ve el Uno Q.
"""
import json
from datetime import datetime

from uno_q import config

_QUEUE = config.DATA_DIR / "sync_queue.jsonl"


def emitir(tipo: str, payload: dict) -> dict:
    """Emite un evento de visión (objeto/persona/ubicación). Envía o encola."""
    evento = {
        "patient_id": config.PATIENT_ID,
        "tipo": tipo,  # objeto_visto | persona_reconocida | ubicacion_objeto
        "payload": payload,
        "ts": datetime.now().isoformat(),
    }
    if config.online() and _enviar(evento):
        _flush()
        return {"enviado": True, **evento}
    _encolar(evento)
    return {"encolado": True, **evento}


def _enviar(evento: dict) -> bool:
    try:
        import requests

        r = requests.post(f"{config.BACKEND_URL}/vision/ingest", json=evento, timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def _encolar(evento: dict):
    with open(_QUEUE, "a", encoding="utf-8") as f:
        f.write(json.dumps(evento, ensure_ascii=False) + "\n")


def _flush():
    """Reenvía la cola pendiente cuando vuelve la red."""
    if not _QUEUE.exists():
        return
    pendientes = [json.loads(l) for l in _QUEUE.read_text(encoding="utf-8").splitlines() if l.strip()]
    quedan = [e for e in pendientes if not _enviar(e)]
    _QUEUE.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in quedan), encoding="utf-8")
