"""API FastAPI — Nino: asistente-guía de rutina (RBAC + criticidad + confirmación + alertas).

Arranque:
    python -m backend.db.seed          # paciente + rutina del día
    python -m backend.rag.ingest       # carga el PKG (twin del paciente)
    uvicorn backend.main:app --reload  # API en :8000/docs
"""
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import select

from backend.db.models import Actividad, Alerta, Patient, Vital, get_session, init_db
from backend.orchestrator.router import route
from backend.routine import engine as routine
from backend.ses import personalizer
from backend.vitals import estimate
from backend.risk import engine as risk_engine

app = FastAPI(title="Nino — API asistente-guía de rutina")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
def _startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- Chat multi-rol (RBAC) ----------
class ChatIn(BaseModel):
    rol: str
    mensaje: str
    patient_id: int = 1


@app.post("/chat")
def chat(body: ChatIn):
    return route(body.rol, body.mensaje, body.patient_id)


@app.get("/patients/{pid}")
def get_patient(pid: int):
    with get_session() as s:
        p = s.exec(select(Patient).where(Patient.id == pid)).first()
    return p or {"error": "no encontrado"}


# ---------- Rutina + criticidad ----------
@app.get("/routine/{pid}/today")
def routine_today(pid: int):
    return routine.plan_dia(pid)


class ProcesarIn(BaseModel):
    receptividad: float = 0.6  # 1=receptivo, 0=irritable (inferido de la conversación)


@app.post("/routine/{pid}/procesar")
def routine_procesar(pid: int, body: ProcesarIn = ProcesarIn()):
    """Evalúa pendientes con el motor de criticidad → recordatorios + alertas al cuidador."""
    return {"recordatorios": routine.procesar_pendientes(pid, body.receptividad)}


class ActividadIn(BaseModel):
    patient_id: int = 1
    nombre: str
    tipo: str = "actividad"
    criticidad_base: float = 0.5
    hora: str = "08:00"
    ventana_min: int = 60
    fecha: str | None = None


@app.post("/actividades")
def crear_actividad(body: ActividadIn):
    with get_session() as s:
        a = Actividad(
            patient_id=body.patient_id, nombre=body.nombre, tipo=body.tipo,
            criticidad_base=body.criticidad_base, hora=body.hora, ventana_min=body.ventana_min,
            fecha=body.fecha or datetime.now().date().isoformat(),
        )
        s.add(a)
        s.commit()
        s.refresh(a)
    return {"ok": True, "id": a.id}


@app.post("/actividades/{aid}/confirmar")
def confirmar_actividad(aid: int):
    return routine.confirmar(aid)


@app.post("/actividades/{aid}/rechazar")
def rechazar_actividad(aid: int):
    return routine.rechazar(aid)


@app.get("/actividades/{aid}/evaluar")
def evaluar_actividad(aid: int, receptividad: float = 0.6):
    with get_session() as s:
        a = s.get(Actividad, aid)
    if not a:
        return {"error": "no encontrada"}
    return routine.evaluar_actividad(a, receptividad)


# ---------- Alertas al cuidador ----------
@app.get("/alertas/{pid}")
def listar_alertas(pid: int, solo_pendientes: bool = True):
    with get_session() as s:
        q = select(Alerta).where(Alerta.patient_id == pid).order_by(Alerta.timestamp.desc())
        alertas = s.exec(q).all()
    if solo_pendientes:
        alertas = [a for a in alertas if not a.atendida]
    return [{"id": a.id, "nivel": a.nivel, "motivo": a.motivo,
             "ts": a.timestamp.isoformat(), "atendida": a.atendida} for a in alertas]


@app.post("/alertas/{aid}/atender")
def atender_alerta(aid: int):
    with get_session() as s:
        a = s.get(Alerta, aid)
        if not a:
            return {"error": "no encontrada"}
        a.atendida = True
        s.add(a)
        s.commit()
    return {"ok": True}


# ---------- Vitales (smartwatch PPG) ----------
class VitalIn(BaseModel):
    patient_id: int = 1
    hr: int
    hrv_ms: float = 0.0
    pasos: int = 0


@app.post("/vitals")
def ingest_vital(body: VitalIn):
    with get_session() as s:
        p = s.exec(select(Patient).where(Patient.id == body.patient_id)).first()
        edad = p.edad if p else 75
        bp = estimate.estimar_presion(body.hr, body.hrv_ms, edad)
        v = Vital(patient_id=body.patient_id, hr=body.hr, hrv_ms=body.hrv_ms, pasos=body.pasos,
                  bp_sys_est=bp["bp_sys_est"], bp_dia_est=bp["bp_dia_est"])
        s.add(v)
        s.commit()
    return {"ok": True, **bp}


@app.get("/vitals/{pid}")
def listar_vitals(pid: int, limit: int = 50):
    with get_session() as s:
        vs = s.exec(select(Vital).where(Vital.patient_id == pid)
                    .order_by(Vital.timestamp.desc())).all()
    return [{"ts": v.timestamp.isoformat(), "hr": v.hr, "hrv_ms": v.hrv_ms, "pasos": v.pasos,
             "bp_sys_est": v.bp_sys_est, "bp_dia_est": v.bp_dia_est} for v in vs[:limit]]


# ---------- Reportes (equipo de cuidado) ----------
@app.get("/reporte/{pid}/adherencia")
def reporte_adherencia(pid: int):
    return routine.reporte_adherencia(pid)


@app.get("/reporte/{pid}/jornada")
def reporte_jornada(pid: int):
    """Twin de la jornada: vista consolidada del día (rutina + adherencia + alertas + vitales)."""
    plan = routine.plan_dia(pid)
    with get_session() as s:
        alertas = s.exec(select(Alerta).where(Alerta.patient_id == pid, Alerta.atendida == False)).all()  # noqa: E712
        v = s.exec(select(Vital).where(Vital.patient_id == pid).order_by(Vital.timestamp.desc())).first()
    return {
        "fecha": plan["fecha"],
        "actividades": plan["actividades"],
        "adherencia": routine.reporte_adherencia(pid),
        "alertas_pendientes": [{"id": a.id, "nivel": a.nivel, "motivo": a.motivo} for a in alertas],
        "ultimo_vital": ({"hr": v.hr, "bp_sys_est": v.bp_sys_est, "bp_dia_est": v.bp_dia_est} if v else None),
    }


# ---------- Riesgo global (fuzzy-bayesiano, capa cloud) ----------
@app.post("/riesgo/{pid}/evaluar")
def riesgo_evaluar(pid: int):
    return risk_engine.evaluar_riesgo_global(pid)


# ---------- Personalización cultural (no cognitiva) ----------
@app.get("/ses/{pid}/perfil")
def ses_perfil(pid: int):
    with get_session() as s:
        p = s.exec(select(Patient).where(Patient.id == pid)).first()
    if not p:
        return {"error": "no encontrado"}
    return {"perfil": personalizer.perfil_para_prompt(p.ses_metadata)}
