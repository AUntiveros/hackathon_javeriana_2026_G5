"""Puente MCU (STM32) ↔ Linux del Uno Q.

Lee las líneas JSON de biométricos que emite el sketch del MCU por Serial y expone el último
estado; envía comandos (p.ej. 'remind' para vibrar). Degrada a stub si no hay puerto serial.

En Arduino App Lab el puente interno MCU↔Linux puede exponerse distinto (mensajería de Bricks);
si es así, reemplazar `_abrir()` por esa API. El resto de la lógica no cambia.
"""
import json
import os
import threading
import time

# Puerto del puente interno del Uno Q (confirmar en la placa; ej. /dev/ttyACM0 o el que exponga App Lab)
SERIAL_PORT = os.environ.get("UNOQ_MCU_PORT", "/dev/ttyACM0")
BAUD = 115200

_latest = {"hr": 0, "steps": 0, "act": "quieto", "fall": False, "sos": False, "stub": True}
_serial = None
_lock = threading.Lock()


def _abrir():
    global _serial
    try:
        import serial  # pyserial
        _serial = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
        return True
    except Exception:
        _serial = None
        return False


def _leer_loop():
    while _serial is not None:
        try:
            line = _serial.readline().decode(errors="ignore").strip()
            if line.startswith("{"):
                data = json.loads(line)
                with _lock:
                    _latest.update(data)
                    _latest["stub"] = False
        except Exception:
            time.sleep(0.2)


def iniciar() -> bool:
    """Abre el serial y arranca el hilo de lectura. Devuelve False si no hay hardware (usa stub)."""
    if _abrir():
        threading.Thread(target=_leer_loop, daemon=True).start()
        return True
    return False


def biometricos() -> dict:
    with _lock:
        return dict(_latest)


def enviar_comando(cmd: str):
    """Envía un comando al MCU (p.ej. 'remind' para vibrar)."""
    if _serial is not None:
        try:
            _serial.write((cmd + "\n").encode())
        except Exception:
            pass
