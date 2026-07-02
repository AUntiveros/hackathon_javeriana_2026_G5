"""Asistente de voz del Uno Q — altavoz paralelo que comparte funciones con la app.

Enruta lo que oye:
  - Comando de entorno (¿qué es esto?, ¿dónde dejé…?, ¿quién me habla?) -> visión local (app.py).
  - Conversación general -> chatbot online (backend /chat, rol paciente) si hay red;
    offline -> respuesta local sencilla.

STT/TTS son pluggables y degradan a texto/print para desarrollar sin micrófono:
  - STT online: Gemini/Google; offline: vosk (modelo ES aparte).
  - TTS online: gTTS; offline: piper/espeak-ng. Sin audio: imprime.
"""
from uno_q import app as gafas
from uno_q import config

_COMANDOS_VISION = ("que es esto", "qué es esto", "que veo", "qué veo", "donde esta", "dónde está",
                    "donde deje", "dónde dejé", "quien me habla", "quién me habla", "quien es",
                    "esto es mi", "guarda esto como", "estoy en", "estamos en", "quien soy")


def hablar(texto: str):
    """TTS. Online gTTS; offline espeak; sin audio imprime."""
    try:
        if config.online():
            from gtts import gTTS
            import tempfile, os
            f = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            gTTS(texto, lang="es").save(f.name)
            _reproducir(f.name)
            os.unlink(f.name)
            return
    except Exception:
        pass
    try:
        import subprocess
        subprocess.run(["espeak-ng", "-v", "es", texto], check=False)
        return
    except Exception:
        pass
    print(f"[TTS] {texto}")


def _reproducir(path: str):
    import subprocess
    for cmd in (["mpg123", "-q", path], ["ffplay", "-nodisp", "-autoexit", path]):
        try:
            subprocess.run(cmd, check=True)
            return
        except Exception:
            continue


def escuchar() -> str:
    """STT. Aquí va vosk (offline) o Gemini/Google (online). Dev: input de texto."""
    # TODO device: micrófono (sounddevice) -> vosk/Gemini. Dev fallback:
    try:
        return input("🎤 (habla/escribe)> ").strip()
    except (EOFError, KeyboardInterrupt):
        return "salir"


def _chatbot(texto: str) -> str:
    """Conversación general -> backend /chat (rol paciente) online; offline respuesta local."""
    if config.online():
        try:
            import requests
            r = requests.post(
                f"{config.BACKEND_URL}/chat",
                json={"rol": "paciente", "mensaje": texto, "patient_id": config.PATIENT_ID},
                timeout=5,
            )
            return r.json().get("respuesta", "…")
        except Exception:
            pass
    return "Estoy aquí con usted. Ahora mismo no tengo conexión, pero podemos conversar."


def responder(texto: str) -> str:
    t = texto.lower()
    if any(c in t for c in _COMANDOS_VISION):
        return gafas.procesar(texto)  # función compartida con la app
    return _chatbot(texto)


def loop():
    print(f"[Voz Uno Q] modo={config.MODE} online={config.online()}")
    while True:
        texto = escuchar()
        if texto.lower() in {"salir", "exit", "quit"}:
            break
        resp = responder(texto)
        hablar(resp)


if __name__ == "__main__":
    loop()
