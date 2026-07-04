import inspect
import pathlib

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


def test_main_no_importa_risk_engine_a_nivel_de_modulo():
    """El import de backend.risk.engine debe ser perezoso (dentro del endpoint),
    NO a nivel de módulo — así un fallo de pgmpy al construir la red bayesiana
    (backend/risk/bayes_engine.py) no tumba el arranque de toda la API, solo
    la ruta /riesgo/{pid}/evaluar. Verificamos esto estructuralmente: el import
    de backend.risk.engine debe vivir dentro del cuerpo de riesgo_evaluar, no
    en el nivel superior del módulo main.py (lo cual ya está probado indirectamente
    por el hecho de que TestClient(app) — usado en este archivo — importa
    backend.main sin depender de que backend.risk se importe con éxito primero).
    """
    import backend.main as main_module

    codigo = pathlib.Path(main_module.__file__).read_text(encoding="utf-8")
    lineas = codigo.splitlines()

    # No debe existir un import de backend.risk.engine fuera de una función
    # (i.e. sin indentación, a nivel de módulo).
    for linea in lineas:
        if "from backend.risk import engine" in linea:
            assert linea.startswith(" ") or linea.startswith("\t"), (
                "el import de backend.risk.engine debe estar dentro del cuerpo "
                "de la función del endpoint (import perezoso), no a nivel de módulo"
            )

    # El import perezoso sí debe existir dentro de riesgo_evaluar.
    fuente_endpoint = inspect.getsource(main_module.riesgo_evaluar)
    assert "from backend.risk import engine" in fuente_endpoint
