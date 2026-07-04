from sqlmodel import select

from backend.db.models import Alerta, get_session, init_db
from backend.risk import engine

PID = 999996


def _limpiar():
    with get_session() as s:
        for a in s.exec(select(Alerta).where(Alerta.patient_id == PID)).all():
            s.delete(a)
        s.commit()


def test_tier_mapping():
    assert engine._tier(0.10) == "ninguna"
    assert engine._tier(0.45) == "preventivo"
    assert engine._tier(0.70) == "agudo_moderado"
    assert engine._tier(0.90) == "crisis"


def test_evaluar_riesgo_global_crea_alerta_en_crisis(monkeypatch):
    init_db()
    _limpiar()
    monkeypatch.setattr(engine, "_calcular_evidencias", lambda pid: (0.9, 0.9, 0.9))
    resultado = engine.evaluar_riesgo_global(PID)
    assert resultado["tier"] == "crisis"
    assert resultado["p_descompensacion"] > 0.85
    with get_session() as s:
        alertas = s.exec(select(Alerta).where(Alerta.patient_id == PID)).all()
    assert len(alertas) == 1
    assert alertas[0].nivel == "alto"
    _limpiar()


def test_evaluar_riesgo_global_no_crea_alerta_si_normal(monkeypatch):
    init_db()
    _limpiar()
    monkeypatch.setattr(engine, "_calcular_evidencias", lambda pid: (0.05, 0.05, 0.05))
    resultado = engine.evaluar_riesgo_global(PID)
    assert resultado["tier"] == "ninguna"
    with get_session() as s:
        alertas = s.exec(select(Alerta).where(Alerta.patient_id == PID)).all()
    assert len(alertas) == 0
    _limpiar()


def test_evaluar_riesgo_global_es_idempotente_no_duplica_alerta(monkeypatch):
    """Llamar el endpoint dos veces seguidas (cron/polling) con el mismo riesgo alto
    no debe crear una segunda alerta sin atender — solo debe existir una."""
    init_db()
    _limpiar()
    try:
        monkeypatch.setattr(engine, "_calcular_evidencias", lambda pid: (0.9, 0.9, 0.9))
        engine.evaluar_riesgo_global(PID)
        engine.evaluar_riesgo_global(PID)
        with get_session() as s:
            alertas = s.exec(
                select(Alerta).where(Alerta.patient_id == PID, Alerta.atendida == False)  # noqa: E712
            ).all()
        assert len(alertas) == 1
    finally:
        _limpiar()
