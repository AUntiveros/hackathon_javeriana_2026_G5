"""Modelos de datos (SQLModel) — núcleo mínimo del Gemelo Cognitivo.

Schema en spec §5. Los campos ricos (metadata SES, features, payload) van como JSON.
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
    ses_metadata: dict = Field(default_factory=dict, sa_column=Column(JSON))
    rutina_base: dict = Field(default_factory=dict, sa_column=Column(JSON))


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tipo: str  # medicacion | actividad | conversacion | alerta | cita | salida
    payload: dict = Field(default_factory=dict, sa_column=Column(JSON))
    estado: str = "pendiente"  # pendiente | hecho | omitido


class Biomarker(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    categoria: str = ""  # prosodico | acustico | lexico | sintactico | semantico
    features: dict = Field(default_factory=dict, sa_column=Column(JSON))
    riesgo_score: float = 0.0
    modelo_version: str = "stub"


class TwinSnapshot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    estado_cognitivo: str = ""
    estado_emocional: str = ""
    riesgo: float = 0.0
    autonomia: float = 1.0
    adherencia: float = 1.0
    carga_cuidador: float = 0.0


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
