"""Memoria espacial aumentada — dónde vio cada objeto por última vez.

Idea casi inédita (Hackathon_Master §6.7): "¿dónde dejé mi celular?" -> "en la mesa gris hace 20
minutos". SQLite local; la zona la fija el usuario por voz ("estoy en la sala") o el contexto.
Futuro: reforzar con AirTag/UWB.
"""
import sqlite3
from datetime import datetime

from uno_q import config
from uno_q.vision import my_objects


def _conn():
    c = sqlite3.connect(config.SPATIAL_DB)
    c.execute(
        """CREATE TABLE IF NOT EXISTS sightings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clase TEXT, etiqueta TEXT, zona TEXT, ts TEXT)"""
    )
    return c


def registrar(clase: str, zona: str):
    """Registra que se vio un objeto en una zona (ahora)."""
    etiqueta = my_objects.resolver(clase)
    c = _conn()
    c.execute(
        "INSERT INTO sightings(clase,etiqueta,zona,ts) VALUES(?,?,?,?)",
        (clase, etiqueta, zona, datetime.now().isoformat()),
    )
    c.commit()
    c.close()


def _humanizar_delta(ts_iso: str) -> str:
    delta = datetime.now() - datetime.fromisoformat(ts_iso)
    m = int(delta.total_seconds() // 60)
    if m < 1:
        return "hace un momento"
    if m < 60:
        return f"hace {m} minuto{'s' if m != 1 else ''}"
    h = m // 60
    return f"hace {h} hora{'s' if h != 1 else ''}"


def donde_esta(clase: str) -> str:
    """Consulta el último avistamiento de un objeto (por clase)."""
    c = _conn()
    row = c.execute(
        "SELECT etiqueta,zona,ts FROM sightings WHERE clase=? ORDER BY ts DESC LIMIT 1",
        (clase,),
    ).fetchone()
    c.close()
    if not row:
        etiqueta = my_objects.resolver(clase)
        return f"No recuerdo dónde vi {etiqueta} por última vez."
    etiqueta, zona, ts = row
    return f"Vi {etiqueta} en {zona} {_humanizar_delta(ts)}."


def buscar_por_texto(texto: str) -> str:
    """Resuelve una consulta libre ('dónde está mi celular') a una clase conocida."""
    t = texto.lower()
    c = _conn()
    clases = [r[0] for r in c.execute("SELECT DISTINCT clase FROM sightings").fetchall()]
    c.close()
    for clase in clases:
        etiqueta = my_objects.resolver(clase).lower()
        if clase in t or any(w in t for w in etiqueta.split() if len(w) > 3):
            return donde_esta(clase)
    return "No tengo registro de ese objeto todavía."
