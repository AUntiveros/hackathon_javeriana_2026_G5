"""Role Router = RBAC. Enruta el mensaje al agente del rol y arma su contexto según scope.

Este es el corazón del RBAC del chatbot: cada rol ve datos y usa tools distintas.
"""
from backend.orchestrator import agents, guardrails, tools
from backend.ses import personalizer


def route(rol: str, mensaje: str, patient_id: int = 1) -> dict:
    if rol not in agents.ROLES:
        return {"error": f"rol desconocido: {rol}", "roles_validos": list(agents.ROLES)}

    patient = tools.get_patient(patient_id)
    ses = patient.ses_metadata if patient else {}
    perfil_ses = personalizer.perfil_para_prompt(ses)

    # Construir contexto según scope del rol (RBAC en acción)
    cfg = agents.ROLES[rol]
    contexto_parts = []

    if "consultar_pkg" in cfg.tools:
        docs = tools.consultar_pkg(mensaje, k=3)
        contexto_parts.append("Memoria del paciente:\n" + "\n".join(f"- {d}" for d in docs))

    if "rutina_hoy" in cfg.tools:
        rut = tools.rutina_hoy(patient_id)
        contexto_parts.append(f"Rutina de hoy y su estado: {rut}")

    if "reporte_adherencia" in cfg.tools:
        rep = tools.reporte_adherencia(patient_id)
        contexto_parts.append(f"Datos reales de adherencia/vitales (usa solo estos, NO evalúes deterioro cognitivo): {rep}")

    if "sugerir_contacto" in cfg.tools:
        sug = tools.sugerir_contacto(patient_id)
        contexto_parts.append(f"Sugerencia de conexión: {sug}")

    contexto = "\n\n".join(contexto_parts) if contexto_parts else "(sin contexto adicional)"

    texto = agents.responder(rol, mensaje, contexto, perfil_ses)
    texto = guardrails.aplicar(rol, texto)

    return {
        "rol": rol,
        "patient_id": patient_id,
        "respuesta": texto,
        "scope": cfg.scope,
        "tools_disponibles": cfg.tools,
    }
