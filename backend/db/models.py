"""Modelos de datos (SQLModel) — asistente-guía de rutina (Nino).

Foco: actividades programadas + confirmación + alertas al cuidador + vitales (smartwatch).
NADA de evaluación cognitiva (prohibido). Los campos ricos van como JSON.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel, create_engine, Session

DB_PATH = "backend/app.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apodo: str = ""
    edad: int = 0
    sexo: str = ""
    diagnostico: str = ""
    personalidad: str = ""
    ses_metadata: dict = Field(default_factory=dict, sa_column=Column(JSON))  # personalización cultural
    cuidadores: list = Field(default_factory=list, sa_column=Column(JSON))    # ids/nombres de la red


class Actividad(SQLModel, table=True):
    """Una rutina programada. El motor de criticidad decide cuánto insistir/escalar."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    nombre: str
    tipo: str  # medicacion | comida | cita | autocuidado | hobby | actividad
    criticidad_base: float = 0.5      # 0-1 (medicacion/comida ~0.9; hobby ~0.2)
    hora: str = "08:00"                # HH:MM programada
    ventana_min: int = 60              # tolerancia antes de considerarla retrasada
    estado: str = "pendiente"          # pendiente | confirmada | omitida | reprogramada
    fecha: str = ""                    # YYYY-MM-DD (día al que aplica)
    n_recordatorios: int = 0
    n_rechazos: int = 0
    detalle: dict = Field(default_factory=dict, sa_column=Column(JSON))


class Alerta(SQLModel, table=True):
    """Aviso al cuidador cuando algo (crítico) no se cumple."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    actividad_id: Optional[int] = Field(default=None, foreign_key="actividad.id")
    nivel: str = "medio"               # bajo | medio | alto
    motivo: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    atendida: bool = False


class Vital(SQLModel, table=True):
    """Signos del smartwatch (PPG). Cardiovascular, NO cognitivo."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    hr: int = 0
    hrv_ms: float = 0.0
    bp_sys_est: Optional[int] = None   # presión sistólica ESTIMADA (no invasiva, no diagnóstica)
    bp_dia_est: Optional[int] = None
    fuente: str = "smartwatch"


class Event(SQLModel, table=True):
    """Log genérico: conversación, ubicación, confirmaciones."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tipo: str
    payload: dict = Field(default_factory=dict, sa_column=Column(JSON))


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
