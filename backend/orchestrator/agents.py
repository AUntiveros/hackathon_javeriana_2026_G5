"""Definición de los 5 agentes de rol (RBAC) y la llamada al LLM.

Cada rol: system prompt, tono, scope de datos y tools permitidas (matriz spec §6).
LLM: Gemini 2.5 Flash. Si no hay GEMINI_API_KEY, usa una respuesta plantillada (modo offline dev).
"""
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


@dataclass
class RolConfig:
    nombre: str
    system_prompt: str
    tools: list[str] = field(default_factory=list)
    scope: list[str] = field(default_factory=list)


ROLES: dict[str, RolConfig] = {
    "paciente": RolConfig(
        "paciente",
        "Eres el compañero de IA de un adulto mayor con Alzheimer leve. Habla cálido, sencillo, "
        "frases cortas, de 'usted'. Usa su memoria (contexto) para recordarle personas y hechos "
        "con cariño y fomentar que hable de sus recuerdos (reminiscencia). NUNCA lo alarmes ni "
        "des diagnósticos. Si no sabes algo, no lo inventes.",
        tools=["consultar_pkg", "rutina_hoy"],
        scope=["pkg", "rutina"],
    ),
    "cuidador": RolConfig(
        "cuidador",
        "Eres el copiloto del cuidador (cuidador aumentado). Tono práctico y empático. Da pasos "
        "accionables: qué preguntar, qué evitar, cuándo intervenir, cómo mantener al paciente "
        "activo sin repetir. Nunca reemplazas el juicio del cuidador.",
        tools=["rutina_hoy", "reporte_adherencia", "sugerir_contacto"],
        scope=["rutina", "adherencia", "alertas"],
    ),
    "medico": RolConfig(
        "medico",
        "Eres asistente del personal de salud. Tono técnico, conciso, con fuentes. Resume señales "
        "clínicas del habla y del sensado usando SOLO datos reales de las herramientas. No "
        "inventes cifras. No sustituyes la decisión clínica.",
        tools=["reporte_adherencia"],
        scope=["adherencia", "vitales"],
    ),
    "familiar": RolConfig(
        "familiar",
        "Ayudas a un familiar a conectar mejor con el paciente. Tono cercano y motivador. Sugiere "
        "cuándo llamar y prepara el contexto de la conversación (temas, recuerdos). No invadas la "
        "privacidad del paciente.",
        tools=["sugerir_contacto", "consultar_pkg"],
        scope=["estado_general", "temas"],
    ),
    "comunidad": RolConfig(
        "comunidad",
        "Conectas al paciente con pares de intereses comunes para combatir el aislamiento. Tono "
        "social e inclusivo. No expongas datos sensibles.",
        tools=["sugerir_contacto"],
        scope=["intereses"],
    ),
}


def _gemini(system_prompt: str, user_prompt: str) -> str | None:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key or "PEGA" in api_key:
        return None  # sin key real -> modo offline plantillado
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        system_instruction=system_prompt,
    )
    return model.generate_content(user_prompt).text


def responder(rol: str, mensaje: str, contexto: str, perfil_ses: str) -> str:
    cfg = ROLES[rol]
    user_prompt = f"{perfil_ses}\n\n{contexto}\n\nMensaje: {mensaje}\n\nResponde:"
    out = _gemini(cfg.system_prompt, user_prompt)
    if out is not None:
        return out
    # Fallback offline (sin API key) — permite desarrollar el flujo completo sin red
    return (
        f"[modo offline · rol {rol}] No hay GEMINI_API_KEY configurada. "
        f"Contexto recuperado:\n{contexto}"
    )
