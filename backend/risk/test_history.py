from datetime import date, timedelta

import pytest
from sqlmodel import select

from backend.db.models import Actividad, get_session, init_db
from backend.risk import history

PID = 999995  # paciente de prueba, no colisiona con el sembrado (id=1)


def _fecha(dias_atras: int) -> str:
    return (date.today() - timedelta(days=dias_atras)).isoformat()


def _limpiar():
    with get_session() as s:
        for a in s.exec(select(Actividad).where(Actividad.patient_id == PID)).all():
            s.delete(a)
        s.commit()


def test_sin_historial_devuelve_prior_neutro():
    init_db()
    _limpiar()
    assert history.tasa_historica(PID, "medicacion") == 0.5


def test_incumplimiento_historico_sube_la_tasa():
    init_db()
    _limpiar()
    try:
        with get_session() as s:
            for i in range(1, 6):
                s.add(Actividad(patient_id=PID, nombre="test", tipo="medicacion",
                                 criticidad_base=0.9, hora="08:00", fecha=_fecha(i),
                                 estado="pendiente"))
            s.commit()
        tasa = history.tasa_historica(PID, "medicacion")
        assert tasa == pytest.approx((5 + 1) / (5 + 2))
    finally:
        _limpiar()


def test_cumplimiento_historico_baja_la_tasa():
    init_db()
    _limpiar()
    try:
        with get_session() as s:
            for i in range(1, 6):
                s.add(Actividad(patient_id=PID, nombre="test", tipo="medicacion",
                                 criticidad_base=0.9, hora="08:00", fecha=_fecha(i),
                                 estado="confirmada"))
            s.commit()
        tasa = history.tasa_historica(PID, "medicacion")
        assert tasa == pytest.approx((0 + 1) / (5 + 2))
    finally:
        _limpiar()
