"""Estimación NO invasiva de presión arterial a partir de señales PPG del smartwatch.

CONCEPTO / PROTOTIPO. No es diagnóstico ni medición clínica: es una estimación por inferencia,
pensada para monitoreo cardiovascular de pacientes hipertensos (la mayoría de pacientes con
Alzheimer lo son). No evalúa deterioro cognitivo.

En producción: modelo entrenado sobre PPG (morfología de onda, PTT) calibrado por paciente.
Aquí: heurística explicable a partir de FC y variabilidad, para poblar la demo.
"""


def estimar_presion(hr: int, hrv_ms: float, edad: int = 75) -> dict:
    """Estimación gruesa de presión (mmHg). Marcado como estimado, no clínico."""
    # Heurística: FC alta y baja variabilidad tienden a asociarse a mayor presión.
    sys_base = 118 + 0.25 * max(0, hr - 70) - 0.05 * hrv_ms + 0.15 * max(0, edad - 65)
    dia_base = 76 + 0.15 * max(0, hr - 70) - 0.03 * hrv_ms
    sys_est = int(max(90, min(190, sys_base)))
    dia_est = int(max(55, min(120, dia_base)))
    categoria = "normal"
    if sys_est >= 140 or dia_est >= 90:
        categoria = "hipertensión"
    elif sys_est >= 130 or dia_est >= 85:
        categoria = "elevada"
    return {"bp_sys_est": sys_est, "bp_dia_est": dia_est, "categoria": categoria,
            "nota": "Estimación no invasiva por PPG. No es diagnóstico clínico."}
