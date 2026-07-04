"""Demo end-to-end del RAG: retriever + Gemini con rol Paciente.

Prototipo mínimo para validar el RAG YA, antes del orquestador completo.
Requiere GEMINI_API_KEY en backend/.env y haber corrido `python -m backend.rag.ingest`.

Uso:
    python -m backend.rag.demo_chat "¿quién es Sofía?"
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from backend.rag.retriever import context_block

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

SYSTEM_PACIENTE = """Eres el compañero de IA de Don Manuel, un adulto mayor de 78 años con
Alzheimer leve, ex-agricultor quechuahablante de zona rural. Habla cálido, sencillo, con
frases cortas y respetuoso (trátalo de 'usted', dile 'Don Manuel'). Usa el contexto de su
memoria para recordarle personas y hechos con cariño. NUNCA lo alarmes ni le des diagnósticos.
Si no sabes algo, no lo inventes. Fomenta que hable de sus recuerdos."""


def responder(mensaje: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        system_instruction=SYSTEM_PACIENTE,
    )
    ctx = context_block(mensaje, k=3)
    prompt = f"{ctx}\n\nDon Manuel dice: {mensaje}\n\nResponde:"
    return model.generate_content(prompt).text


if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "No me acuerdo quién me llamó ayer."
    print("Don Manuel:", msg)
    print("IA:", responder(msg))
