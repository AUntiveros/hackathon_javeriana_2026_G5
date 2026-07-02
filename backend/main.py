"""API FastAPI — orquestador del ecosistema Alzheimer.

Arranque:
    python -m backend.db.seed          # una vez, puebla la DB
    python -m backend.rag.ingest       # una vez, carga el PKG
    uvicorn backend.main:app --reload  # levanta la API en :8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import select

from backend.biomarkers import extract, predict
from backend.db.models import Biomarker, Event, Patient, TwinSnapshot, get_session, init_db
from backend.orchestrator.router import route
from backend.routine.engine import plan_dia
from backend.ses import personalizer

app = FastAPI(title="Ecosistema Alzheimer — API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    init_db()


class ChatIn(BaseModel):
    rol: str
    mensaje: str
    patient_id: int = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(body: ChatIn):
    """Punto único del chatbot multi-rol (RBAC)."""
    return route(body.rol, body.mensaje, body.patient_id)


@app.get("/patients/{pid}")
def get_patient(pid: int):
    with get_session() as s:
        p = s.exec(select(Patient).where(Patient.id == pid)).first()
    if not p:
        return {"error": "no encontrado"}
    return p


@app.get("/routine/{pid}/today")
def routine_today(pid: int):
    return plan_dia(pid)


@app.get("/twin/{pid}/trend")
def twin_trend(pid: int):
    with get_session() as s:
        bios = s.exec(
            select(Biomarker).where(Biomarker.patient_id == pid).order_by(Biomarker.timestamp)
        ).all()
    return [
        {"t": b.timestamp.isoformat(), "riesgo": b.riesgo_score, **b.features} for b in bios
    ]


@app.get("/twin/{pid}/snapshot")
def twin_snapshot(pid: int):
    with get_session() as s:
        snap = s.exec(
            select(TwinSnapshot)
            .where(TwinSnapshot.patient_id == pid)
            .order_by(TwinSnapshot.timestamp.desc())
        ).first()
    return snap or {"error": "sin snapshot"}


class AnalyzeIn(BaseModel):
    patient_id: int = 1
    transcript: str | None = None
    audio_path: str | None = None
    features: dict | None = None


@app.post("/biomarkers/analyze")
def biomarkers_analyze(body: AnalyzeIn):
    """Extrae features (o usa las dadas), predice riesgo y lo ajusta por equidad SES."""
    with get_session() as s:
        p = s.exec(select(Patient).where(Patient.id == body.patient_id)).first()
    if not p:
        return {"error": "paciente no encontrado"}
    feats = body.features or extract.extract(body.audio_path, body.transcript)
    return predict.analizar(body.patient_id, feats, p.ses_metadata)


class VisionEventIn(BaseModel):
    patient_id: int = 1
    tipo: str  # objeto_visto | persona_reconocida | ubicacion_objeto
    payload: dict = {}
    ts: str | None = None


@app.post("/vision/ingest")
def vision_ingest(body: VisionEventIn):
    """Recibe lo que ve el Uno Q y lo guarda como evento (alimenta el Gemelo/PKG del asistente)."""
    with get_session() as s:
        e = Event(patient_id=body.patient_id, tipo=f"vision:{body.tipo}", payload=body.payload)
        s.add(e)
        s.commit()
        s.refresh(e)
    return {"ok": True, "event_id": e.id}


@app.get("/vision/{pid}/recent")
def vision_recent(pid: int, limit: int = 20):
    with get_session() as s:
        evs = s.exec(
            select(Event)
            .where(Event.patient_id == pid, Event.tipo.like("vision:%"))
            .order_by(Event.timestamp.desc())
        ).all()
    return [{"tipo": e.tipo, "payload": e.payload, "ts": e.timestamp.isoformat()} for e in evs[:limit]]


@app.get("/ses/{pid}/riesgo")
def ses_riesgo(pid: int, riesgo_bruto: float = 0.6):
    """Demuestra el ajuste de equidad SES sobre un riesgo dado."""
    with get_session() as s:
        p = s.exec(select(Patient).where(Patient.id == pid)).first()
    if not p:
        return {"error": "no encontrado"}
    return personalizer.ajustar_riesgo(riesgo_bruto, p.ses_metadata)
