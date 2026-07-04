import pytest

from backend.risk import bayes_engine


def test_todo_normal_riesgo_bajo():
    p = bayes_engine.inferir_riesgo(0.05, 0.05, 0.05)
    assert p < 0.30


def test_una_sola_senal_alta_no_escala_sola():
    p = bayes_engine.inferir_riesgo(0.9, 0.05, 0.05)
    assert 0.30 <= p < 0.60


def test_tres_senales_altas_simultaneas_cruzan_crisis():
    p = bayes_engine.inferir_riesgo(0.9, 0.9, 0.9)
    assert p > 0.85


def test_dos_senales_altas_quedan_en_rango_agudo_moderado():
    p = bayes_engine.inferir_riesgo(0.9, 0.9, 0.05)
    assert 0.60 <= p < 0.85


def test_valores_conocidos_exactos():
    assert bayes_engine.inferir_riesgo(0.05, 0.05, 0.05) == pytest.approx(0.056, abs=0.01)
    assert bayes_engine.inferir_riesgo(0.9, 0.9, 0.9) == pytest.approx(0.869, abs=0.01)
