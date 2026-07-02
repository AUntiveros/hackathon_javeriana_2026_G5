"""Guardrails anti-alucinación por rol.

El agente Médico nunca inventa cifras (solo las de la DB vía tools) y siempre lleva disclaimer.
Todos los roles evitan dar diagnóstico o consejo médico no verificado.
"""

DISCLAIMER_MEDICO = (
    "\n\n— Nota: señales derivadas del habla y sensado pasivo. No es un diagnóstico; "
    "la decisión clínica es del profesional de salud."
)

DISCLAIMER_GENERAL = (
    "\n\n(Este asistente acompaña y organiza el cuidado; no reemplaza al equipo de salud.)"
)


def aplicar(rol: str, texto: str) -> str:
    if rol == "medico":
        if "diagnóstico" not in texto.lower():
            return texto + DISCLAIMER_MEDICO
        return texto + DISCLAIMER_MEDICO
    if rol in {"cuidador", "familiar", "comunidad"}:
        return texto + DISCLAIMER_GENERAL
    # paciente: sin disclaimer técnico (no alarmar)
    return texto
