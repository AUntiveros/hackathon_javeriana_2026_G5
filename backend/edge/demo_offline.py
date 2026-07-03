"""Demo de operación OFFLINE-FIRST del asistente (sin red, sin LLM).

Prueba tangible de que el núcleo del paciente funciona sin internet: la rutina, el motor de
criticidad, la confirmación y el escalado corren con lógica pura + SQLite local. Solo la
conversación rica necesita nube (con fallback plantillado). Útil para el pitch: "apago el WiFi
y sigue funcionando".

Uso:
    python -m backend.edge.demo_offline
"""
from backend.db.models import Actividad, get_session, init_db
from backend.db.seed import seed
from backend.routine import engine as routine


def _forzar_vencidas():
    """Pone la rutina de hoy en horas pasadas para simular el transcurso del día."""
    horas = ["00:01", "00:05", "00:10", "00:15", "00:20", "00:25"]
    with get_session() as s:
        acts = s.exec(__import__("sqlmodel").select(Actividad)
                      .where(Actividad.fecha == routine._hoy())).all()
        for a, h in zip(acts, horas):
            a.hora = h
            a.ventana_min = 5
            s.add(a)
        s.commit()


def main():
    init_db()
    seed()
    _forzar_vencidas()
    print("=== MODO OFFLINE (sin red, sin LLM) - un dia simulado ===\n")

    # Paciente receptivo por la mañana
    print("[10:00] Paciente receptivo:")
    for r in routine.procesar_pendientes(1, receptividad=0.7):
        flag = "  [!] ALERTA CUIDADOR" if r["alertar_cuidador"] else ""
        print(f"  - {r['nombre']:35} {r['accion']:16} -> {r['mensaje']}{flag}")

    # El paciente confirma la comida, rechaza el hobby
    plan = routine.plan_dia(1)["actividades"]
    comida = next((a for a in plan if a["tipo"] == "comida"), None)
    hobby = next((a for a in plan if a["tipo"] == "hobby"), None)
    if comida:
        routine.confirmar(comida["id"])
        print(f"\n  Paciente: 'ya almorcé' → {comida['nombre']} confirmada")
    if hobby:
        d = routine.rechazar(hobby["id"])["decision"]
        print(f"  Paciente: 'no quiero leer' → {hobby['nombre']}: {d['accion']} (se respeta, no fuerza)")

    print("\n=== Reporte de adherencia (offline) ===")
    rep = routine.reporte_adherencia(1)
    print(f"  Adherencia total: {rep['adherencia_pct']}% | crítica: {rep['adherencia_critica_pct']}% "
          f"| alertas pendientes: {rep['alertas_pendientes']}")
    print("\nTodo esto corrió SIN internet y SIN LLM. La nube solo agrega conversación y reportes.")


if __name__ == "__main__":
    main()
