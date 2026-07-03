"""Mapea clases genéricas detectadas a etiquetas personales del paciente.

Ej: la clase COCO 'cell phone' -> 'tu celular'. Persistido en JSON.
"""
import json

from uno_q import config


def _load() -> dict:
    if config.MYOBJECTS_STORE.exists():
        return json.loads(config.MYOBJECTS_STORE.read_text(encoding="utf-8"))
    return {}


def _save(d: dict):
    config.MYOBJECTS_STORE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def enrolar(clase: str, etiqueta_personal: str):
    """'esto es mi celular' -> enrolar('cell phone', 'tu celular')."""
    d = _load()
    d[clase] = etiqueta_personal
    _save(d)


def resolver(clase: str) -> str:
    """Devuelve la etiqueta personal si existe, si no el nombre genérico traducido."""
    d = _load()
    if clase in d:
        return d[clase]
    return _ES.get(clase, clase)


# Traducción mínima de clases COCO frecuentes (para hablarle al paciente en español)
_ES = {
    "cell phone": "un celular",
    "cup": "una taza",
    "bottle": "una botella",
    "book": "un libro",
    "keyboard": "un teclado",
    "remote": "un control remoto",
    "chair": "una silla",
    "tv": "un televisor",
    "clock": "un reloj",
    "scissors": "unas tijeras",
    "spoon": "una cuchara",
    "person": "una persona",
}
