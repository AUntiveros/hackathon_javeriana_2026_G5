from backend.risk import evidence


def test_grado_olvido_medicacion():
    assert evidence.grado_olvido_medicacion(0) == 0.0
    assert evidence.grado_olvido_medicacion(60) == 0.0
    assert evidence.grado_olvido_medicacion(180) == 1.0
    assert evidence.grado_olvido_medicacion(120) == 0.5


def test_grado_ayuno():
    assert evidence.grado_ayuno(0) == 0.0
    assert evidence.grado_ayuno(60) == 0.0
    assert evidence.grado_ayuno(240) == 1.0
    assert evidence.grado_ayuno(150) == 0.5


def test_grado_sedentarismo():
    assert evidence.grado_sedentarismo(1000, 1000) == 0.0
    assert evidence.grado_sedentarismo(500, 1000) == 0.5
    assert evidence.grado_sedentarismo(100, 1000) == 1.0
    assert evidence.grado_sedentarismo(500, 0) == 0.0  # sin baseline: no alarma falsa
