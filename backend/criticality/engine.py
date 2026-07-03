"""Motor de criticidad — lógica difusa (Mamdani) pura en Python.

Decide, para una actividad pendiente/retrasada, CUÁNTO insistir y si escalar al cuidador,
respetando la autonomía del paciente (NUNCA fuerza; el enforcement de lo crítico = avisar al
cuidador, no coaccionar).

Entradas:
  criticidad   [0-1]  (medicacion/comida ~0.9; hobby ~0.2)
  retraso_min  minutos de retraso respecto a la hora programada
  receptividad [0-1]  (1 = receptivo, 0 = irritable; inferido de la conversación)
  n_rechazos   int    (rechazos recientes de esta actividad)

Salida: dict con accion, insistencia [0-1], tono, alertar_cuidador, y traza explicable.

Sin dependencias externas (portable/edge). Alternativa: scikit-fuzzy (mismo diseño).
"""


def _tri(x, a, b, c):
    """Pertenencia triangular."""
    if x <= a or x >= c:
        return 0.0
    if x == b:
        return 1.0
    if x < b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)


def _grade_up(x, a, b):
    """Rampa creciente (hombro)."""
    if x <= a:
        return 0.0
    if x >= b:
        return 1.0
    return (x - a) / (b - a)


def fuzzify(criticidad, retraso_min, receptividad):
    return {
        "crit_baja": _tri(criticidad, -0.1, 0.15, 0.45),
        "crit_media": _tri(criticidad, 0.3, 0.55, 0.75),
        "crit_alta": _grade_up(criticidad, 0.6, 0.9),
        "ret_nada": _tri(retraso_min, -10, 0, 20),
        "ret_poco": _tri(retraso_min, 10, 35, 60),
        "ret_mucho": _grade_up(retraso_min, 45, 90),
        "rec_baja": _tri(receptividad, -0.1, 0.15, 0.45),
        "rec_media": _tri(receptividad, 0.3, 0.55, 0.75),
        "rec_alta": _grade_up(receptividad, 0.6, 0.9),
    }


# Centroides de los conjuntos de salida "insistencia" [0-1]
_OUT = {"soltar": 0.12, "suave": 0.38, "firme": 0.62, "escalar": 0.9}


def _rules(m, n_rechazos):
    """Devuelve lista de (conjunto_salida, fuerza) disparados."""
    AND = min
    fired = [
        ("escalar", AND(m["crit_alta"], m["ret_mucho"])),
        ("firme", AND(m["crit_alta"], m["ret_poco"])),
        ("firme", AND(m["crit_alta"], m["rec_baja"])),   # crítico + irritable: firme y cálido, no escalar aún
        ("suave", AND(m["crit_media"], m["ret_poco"])),
        ("firme", AND(m["crit_media"], m["ret_mucho"])),
        ("soltar", AND(m["crit_baja"], m["rec_baja"])),  # no crítico + no quiere: soltar sin fricción
        ("suave", AND(m["crit_baja"], m["ret_mucho"])),
        ("suave", AND(m["crit_baja"], m["rec_alta"])),
        ("suave", AND(m["crit_media"], m["rec_alta"])),
    ]
    # rechazo persistente de algo crítico empuja a escalar
    if n_rechazos >= 2:
        fired.append(("escalar", m["crit_alta"]))
    return [(s, f) for s, f in fired if f > 0]


def evaluar(criticidad, retraso_min=0.0, receptividad=0.6, n_rechazos=0) -> dict:
    m = fuzzify(criticidad, retraso_min, receptividad)
    fired = _rules(m, n_rechazos)

    # Defuzzificación por centroides ponderados (agregando por max por conjunto)
    agg = {}
    for s, f in fired:
        agg[s] = max(agg.get(s, 0.0), f)
    if agg:
        num = sum(_OUT[s] * f for s, f in agg.items())
        den = sum(agg.values())
        insistencia = num / den
    else:
        insistencia = 0.2  # sin reglas: sugerencia mínima

    if insistencia < 0.25:
        accion = "soltar"
    elif insistencia < 0.5:
        accion = "sugerir_suave"
    elif insistencia < 0.72:
        accion = "recordar_firme"
    else:
        accion = "escalar_cuidador"

    return {
        "accion": accion,
        "insistencia": round(insistencia, 3),
        "alertar_cuidador": accion == "escalar_cuidador",
        "tono": "cálido y respetuoso (nunca imperativo)",
        "traza": {
            "membresias": {k: round(v, 2) for k, v in m.items() if v > 0},
            "reglas_disparadas": {s: round(max(f for ss, f in fired if ss == s), 2)
                                  for s in {s for s, _ in fired}},
        },
    }
