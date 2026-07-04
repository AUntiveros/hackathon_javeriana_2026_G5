from fastapi.testclient import TestClient
from sqlmodel import select

from backend.db.models import Alerta, get_session, init_db
from backend.main import app
from backend.risk import engine

PID = 999997
client = TestClient(app)


def _limpiar():
    with get_session() as s:
        for a in s.exec(select(Alerta).where(Alerta.patient_id == PID)).all():
            s.delete(a)
        s.commit()


def test_endpoint_riesgo_evaluar_devuelve_tier_crisis(monkeypatch):
    init_db()
    _limpiar()
    monkeypatch.setattr(engine, "_calcular_evidencias", lambda pid: (0.9, 0.9, 0.9))
    r = client.post(f"/riesgo/{PID}/evaluar")
    assert r.status_code == 200
    body = r.json()
    assert body["tier"] == "crisis"
    assert body["patient_id"] == PID
    _limpiar()
