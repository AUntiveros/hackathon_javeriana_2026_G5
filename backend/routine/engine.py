"""Motor de rutina v2 — recordatorios + confirmación + escalado (con motor de criticidad).

Cumple la delimitación oficial: recuerda una actividad, confirma si se hizo, avisa al cuidador si
lo crítico no se cumple. El motor de criticidad decide cuánto insistir SIN forzar al paciente.
"""
from datetime import date, datetime

from sqlmodel import select

from backend.criticality import engine as crit
from backend.db.models import Actividad, Alerta, Event, get_session


def _hoy() -> str:
    return date.today().isoformat()


def _retraso_min(hora: str, ventana: int) -> float:
    """Minutos de retraso respecto a (hora programada + ventana de tolerancia). 0 si aún en ventana."""
    try:
        h, m = map(int, hora.split(":"))
    except Exception:
        return 0.0
    ahora = datetime.now()
    programada = ahora.replace(hour=h, minute=m, second=0, microsecond=0)
    transcurrido = (ahora - programada).total_seconds() / 60.0
    return max(0.0, transcurrido - ventana)


def plan_dia(patient_id: int = 1) -> dict:
    with get_session() as s:
        acts = s.exec(
            select(Actividad).where(Actividad.patient_id == patient_id, Actividad.fecha == _hoy())
            .order_by(Actividad.hora)
        ).all()
    return {
        "patient_id": patient_id,
        "fecha": _hoy(),
        "actividades": [_act_dict(a) for a in acts],
    }


def _act_dict(a: Actividad) -> dict:
    return {"id": a.id, "nombre": a.nombre, "tipo": a.tipo, "hora": a.hora,
            "criticidad": a.criticidad_base, "estado": a.estado,
            "n_recordatorios": a.n_recordatorios, "n_rechazos": a.n_rechazos}


def _mensaje(actividad: Actividad, accion: str) -> str:
    """Genera el recordatorio cálido (nunca imperativo) según la acción y el tipo."""
    n = actividad.nombre.lower()
    if accion == "soltar":
        return f"Está bien, dejamos «{actividad.nombre}» para más tarde. Sin apuro."
    if accion == "sugerir_suave":
        return f"Cuando usted quiera, sería lindo hacer «{actividad.nombre}». ¿Le provoca?"
    if accion == "recordar_firme":
        if actividad.tipo == "medicacion":
            return f"Don Manuel, es momento de su {n}. ¿La tomamos juntos ahora?"
        if actividad.tipo == "comida":
            return f"Ya es hora de {n}. ¿Comemos algo rico?"
        return f"Le recuerdo con cariño: es hora de «{actividad.nombre}». ¿Lo hacemos?"
    if accion == "escalar_cuidador":
        return f"Insisto con cariño en «{actividad.nombre}». (Aviso también a su familia para acompañarlo.)"
    return f"¿Le gustaría hacer «{actividad.nombre}»?"


def evaluar_actividad(actividad: Actividad, receptividad: float = 0.6) -> dict:
    retraso = _retraso_min(actividad.hora, actividad.ventana_min)
    decision = crit.evaluar(actividad.criticidad_base, retraso, receptividad, actividad.n_rechazos)
    decision["retraso_min"] = round(retraso, 1)
    decision["mensaje"] = _mensaje(actividad, decision["accion"])
    return decision


def procesar_pendientes(patient_id: int = 1, receptividad: float = 0.6) -> list[dict]:
    """Evalúa las actividades pendientes/retrasadas de hoy; genera recordatorios y alertas."""
    resultados = []
    with get_session() as s:
        acts = s.exec(
            select(Actividad).where(
                Actividad.patient_id == patient_id,
                Actividad.fecha == _hoy(),
                Actividad.estado == "pendiente",
            )
        ).all()
        for a in acts:
            d = evaluar_actividad(a, receptividad)
            if d["accion"] == "soltar":
                continue  # respeta autonomía: no molesta
            a.n_recordatorios += 1
            if d["alertar_cuidador"]:
                s.add(Alerta(patient_id=patient_id, actividad_id=a.id, nivel="alto",
                             motivo=f"No se completó: {a.nombre}"))
            s.add(a)
            resultados.append({"actividad_id": a.id, "nombre": a.nombre, **d})
        s.commit()
    return resultados


def confirmar(actividad_id: int) -> dict:
    with get_session() as s:
        a = s.get(Actividad, actividad_id)
        if not a:
            return {"error": "actividad no encontrada"}
        a.estado = "confirmada"
        s.add(a)
        s.add(Event(patient_id=a.patient_id, tipo="confirmacion", payload={"actividad": a.nombre}))
        s.commit()
    return {"ok": True, "actividad_id": actividad_id, "estado": "confirmada"}


def rechazar(actividad_id: int) -> dict:
    """El paciente no quiere. Se respeta; el motor decidirá si insistir/soltar/escalar luego."""
    with get_session() as s:
        a = s.get(Actividad, actividad_id)
        if not a:
            return {"error": "actividad no encontrada"}
        a.n_rechazos += 1
        s.add(a)
        s.commit()
        d = evaluar_actividad(a)
    return {"ok": True, "actividad_id": actividad_id, "n_rechazos": a.n_rechazos, "decision": d}


def reporte_adherencia(patient_id: int = 1) -> dict:
    with get_session() as s:
        acts = s.exec(
            select(Actividad).where(Actividad.patient_id == patient_id, Actividad.fecha == _hoy())
        ).all()
        alertas = s.exec(
            select(Alerta).where(Alerta.patient_id == patient_id, Alerta.atendida == False)  # noqa: E712
        ).all()
    total = len(acts)
    confirmadas = sum(1 for a in acts if a.estado == "confirmada")
    criticas = [a for a in acts if a.criticidad_base >= 0.8]
    criticas_ok = sum(1 for a in criticas if a.estado == "confirmada")
    return {
        "patient_id": patient_id,
        "fecha": _hoy(),
        "total_actividades": total,
        "confirmadas": confirmadas,
        "adherencia_pct": round(100 * confirmadas / total, 1) if total else 0,
        "criticas_total": len(criticas),
        "criticas_confirmadas": criticas_ok,
        "adherencia_critica_pct": round(100 * criticas_ok / len(criticas), 1) if criticas else 100,
        "alertas_pendientes": len(alertas),
    }
