from fastapi.testclient import TestClient
from sqlmodel import select

from backend.db.models import Vital, get_session, init_db
from backend.main import app

PID = 999998
client = TestClient(app)


def _limpiar():
    with get_session() as s:
        for v in s.exec(select(Vital).where(Vital.patient_id == PID)).all():
            s.delete(v)
        s.commit()


def test_ingest_vital_guarda_y_devuelve_pasos():
    init_db()
    _limpiar()
    r = client.post("/vitals", json={"patient_id": PID, "hr": 70, "hrv_ms": 40.0, "pasos": 1234})
    assert r.status_code == 200
    r2 = client.get(f"/vitals/{PID}")
    assert r2.json()[0]["pasos"] == 1234
    _limpiar()
