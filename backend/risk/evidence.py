"""Fuzzificación de evidencias para el motor de riesgo global (capa cloud).

Reutiliza las funciones de pertenencia del motor de criticidad por-actividad
(backend/criticality/engine.py) para mantener el mismo lenguaje difuso en ambas capas.
"""
from backend.criticality.engine import _grade_up


def grado_olvido_medicacion(retraso_min: float) -> float:
    """[0-1]: 60min de retraso ya es preocupante, 180min (3h) es 'olvido crítico'."""
    return _grade_up(retraso_min, 60, 180)


def grado_ayuno(retraso_min: float) -> float:
    """[0-1]: 60min sobre la ventana de la comida es 'retraso leve', 240min (4h) es ayuno severo."""
    return _grade_up(retraso_min, 60, 240)


def grado_sedentarismo(pasos_hoy: int, baseline: int) -> float:
    """[0-1]: cuánto cae pasos_hoy respecto al baseline histórico del paciente.
    Sin baseline (paciente nuevo, sin historial de vitales) -> 0.0, no genera falsa alarma."""
    if baseline <= 0:
        return 0.0
    caida = 1 - (pasos_hoy / baseline)
    return _grade_up(caida, 0.3, 0.7)
