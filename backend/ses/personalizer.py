"""Motor de personalización socioeconómica (SES).

Dos funciones:
1. Ajustar la interpretación del riesgo según reserva cognitiva estimada (evita falsos
   positivos en baja escolaridad) — el diferenciador de equidad del proyecto.
2. Producir un perfil SES en texto para inyectar en el prompt del LLM (In-Context Learning),
   estrategia con evidencia 2026 para razonamiento clínico más equitativo.
"""

# Peso de reserva cognitiva por nivel educativo. Más reserva => mismo daño se ve MENOS en el
# habla superficial => hay que ser más cauto para no sub-diagnosticar; MENOS reserva => más
# riesgo de confundir baja escolaridad con deterioro => hay que subir el umbral de alarma.
_ESCOLARIDAD_RESERVA = {
    "sin_estudios": 0.15,
    "primaria_incompleta": 0.25,
    "primaria": 0.35,
    "secundaria": 0.55,
    "tecnica": 0.70,
    "universitaria": 0.85,
    "posgrado": 0.95,
}


def estimar_reserva_cognitiva(ses: dict) -> float:
    """Estima reserva cognitiva [0-1] desde metadata SES."""
    base = _ESCOLARIDAD_RESERVA.get(ses.get("escolaridad", "secundaria"), 0.5)
    idh = float(ses.get("idh_distrital", 0.6))
    ocup_bonus = 0.05 if ses.get("ocupacion_historica") in {"profesor", "profesional"} else 0.0
    bilingue_bonus = 0.05 if ses.get("bilingue") else 0.0
    reserva = 0.6 * base + 0.3 * idh + ocup_bonus + bilingue_bonus
    return round(min(1.0, reserva), 3)


def ajustar_riesgo(riesgo_bruto: float, ses: dict) -> dict:
    """Ajusta el riesgo del modelo por reserva cognitiva y explica el ajuste (trazabilidad).

    Baja reserva -> el umbral de alarma sube (descuenta parte del riesgo atribuible a la baja
    escolaridad, no a la enfermedad), reduciendo falsos positivos en poblaciones vulnerables.
    """
    reserva = estimar_reserva_cognitiva(ses)
    # descuento máximo de 0.15 cuando la reserva es muy baja
    descuento = (1.0 - reserva) * 0.15
    ajustado = max(0.0, min(1.0, riesgo_bruto - descuento))
    return {
        "riesgo_bruto": round(riesgo_bruto, 3),
        "reserva_cognitiva": reserva,
        "descuento_equidad": round(descuento, 3),
        "riesgo_ajustado": round(ajustado, 3),
        "explicacion": (
            f"Reserva cognitiva estimada {reserva} (escolaridad "
            f"'{ses.get('escolaridad','?')}', IDH {ses.get('idh_distrital','?')}). "
            f"Se descuenta {round(descuento,3)} del riesgo para no confundir patrones de habla "
            f"de baja escolaridad con deterioro."
        ),
    }


def perfil_para_prompt(ses: dict) -> str:
    """Perfil SES en texto para In-Context Learning en el prompt del agente."""
    return (
        f"Perfil del paciente: escolaridad {ses.get('escolaridad','?')}, "
        f"zona {ses.get('zona','?')}, lengua materna {ses.get('lengua_materna','?')}"
        f"{' (bilingüe)' if ses.get('bilingue') else ''}, "
        f"ocupación histórica {ses.get('ocupacion_historica','?')}. "
        f"Adapta vocabulario y ejemplos a este contexto cultural; usa lenguaje sencillo."
    )
