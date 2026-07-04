"""Puebla la DB: paciente + rutina del día (actividades con criticidad).

Uso:
    python -m backend.db.seed
"""
import json
from datetime import date, datetime, timedelta
from pathlib import Path

from sqlmodel import select

from backend.db.models import Actividad, Patient, get_session, init_db

SEED_PATH = Path(__file__).resolve().parents[1] / "seed" / "don_manuel.json"


def _hoy() -> str:
    return date.today().isoformat()


def seed():
    init_db()
    data = json.loads(SEED_PATH.read_text(encoding="utf-8"))["patient"]

    with get_session() as s:
        if s.exec(select(Patient).where(Patient.id == 1)).first():
            print("[seed] ya existe el paciente; nada que hacer")
            return

        p = Patient(
            id=1,
            nombre=data["nombre"],
            apodo=data["apodo"],
            edad=data["edad"],
            sexo=data["sexo"],
            diagnostico=data["diagnostico"],
            personalidad=data["personalidad"],
            ses_metadata=data["ses_metadata"],
            cuidadores=[{"nombre": "Rosa (hija)", "rol": "cuidador"}, {"nombre": "Dr. Vera", "rol": "medico"}],
        )
        s.add(p)

        hoy = _hoy()
        cita = (date.today() + timedelta(days=7)).isoformat()
        rutina = [
            ("Pastilla de la memoria (donepezilo)", "medicacion", 0.9, "08:30", 30, {}),
            ("Aseo de la mañana", "autocuidado", 0.6, "09:00", 90, {}),
            ("Almuerzo", "comida", 0.85, "13:00", 60, {}),
            ("Leer el libro de la semana", "hobby", 0.2, "16:00", 180, {}),
            ("Caminata de la tarde", "actividad", 0.35, "17:00", 120,
             {"beneficio": "hipertensión", "pasos_meta": 1500}),
            ("Pastilla de la presión", "medicacion", 0.9, "08:00", 30,
             {"condicion": "hipertensión", "dosis_dia": 3}),
            ("Pastilla de la presión", "medicacion", 0.9, "14:00", 30,
             {"condicion": "hipertensión", "dosis_dia": 3}),
            ("Pastilla de la presión", "medicacion", 0.9, "20:00", 30,
             {"condicion": "hipertensión", "dosis_dia": 3}),
        ]
        for nombre, tipo, crit, hora, ventana, detalle in rutina:
            s.add(Actividad(patient_id=1, nombre=nombre, tipo=tipo, criticidad_base=crit,
                            hora=hora, ventana_min=ventana, fecha=hoy, detalle=detalle))
        # una cita futura
        s.add(Actividad(patient_id=1, nombre="Control con el geriatra", tipo="cita",
                        criticidad_base=0.7, hora="10:00", ventana_min=60, fecha=cita))
        s.commit()
    print("[seed] paciente + rutina del día cargados")


if __name__ == "__main__":
    seed()
