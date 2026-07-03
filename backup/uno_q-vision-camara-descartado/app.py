"""Loop principal del asistente Uno Q — visión + memoria espacial + "mis objetos".

Dev: CLI por texto (funciona sin cámara/modelo, usa stub). Device: se cablea a voz + cámara.

Comandos (dev CLI):
  ver / que es esto           -> captura y detecta; dice qué ve
  esto es mi <etiqueta>       -> enrola el objeto detectado como personal
  estoy en <zona>             -> fija la zona actual (para la memoria espacial)
  donde esta mi <objeto>      -> consulta el último avistamiento
  salir

Ejecutar:
  python -m uno_q.app
"""
from uno_q import config
from uno_q.hardware import bridge
from uno_q.sync import cloud
from uno_q.vision import detector, faces, my_objects, spatial_memory

_zona_actual = "un lugar desconocido"


def _ultimo_detectado():
    frame = detector.capturar()
    dets = detector.detectar(frame)
    return dets[0] if dets else None


def procesar(texto: str) -> str:
    global _zona_actual
    t = texto.lower().strip()

    if t in {"ver", "que es esto", "qué es esto", "que veo", "qué veo"}:
        det = _ultimo_detectado()
        if not det:
            return "No veo nada claro."
        # registrar el avistamiento en la zona actual (alimenta memoria espacial)
        spatial_memory.registrar(det["label"], _zona_actual)
        etiqueta = my_objects.resolver(det["label"])
        # alimentar la database del asistente (sync online / cola offline)
        cloud.emitir("objeto_visto", {"clase": det["label"], "etiqueta": etiqueta})
        cloud.emitir("ubicacion_objeto", {"clase": det["label"], "zona": _zona_actual})
        modo = " (simulado: falta modelo/cámara)" if det.get("stub") else ""
        return f"Veo {etiqueta}{modo}."

    if "quien" in t and ("habla" in t or "es" in t) or t in {"quien soy", "quién soy"}:
        frame = detector.capturar()
        nombre = faces.reconocer(frame)
        cloud.emitir("persona_reconocida", {"nombre": nombre})
        return f"Te está hablando {nombre}." if nombre != "alguien que no reconozco" else f"Veo {nombre}."

    if t.startswith("esto es mi ") or t.startswith("guarda esto como "):
        etiqueta = t.split("mi ", 1)[-1] if "mi " in t else t.split("como ", 1)[-1]
        det = _ultimo_detectado()
        if not det:
            return "No veo un objeto para guardar."
        my_objects.enrolar(det["label"], f"tu {etiqueta}")
        return f"Guardado: cuando vea {det['label']} lo llamaré 'tu {etiqueta}'."

    if t.startswith("estoy en ") or t.startswith("pongo") or t.startswith("estamos en "):
        _zona_actual = t.split("en ", 1)[-1] if "en " in t else t
        return f"Anotado. Zona actual: {_zona_actual}."

    if "donde esta" in t or "dónde está" in t or "donde deje" in t or "dónde dejé" in t:
        return spatial_memory.buscar_por_texto(t)

    if "signos" in t or "como esta mi" in t or "frecuencia" in t or "pulso" in t:
        b = bridge.biometricos()
        modo = " (simulado: falta el MCU/sensores)" if b.get("stub") else ""
        return f"Su pulso es {b['hr']} por minuto, lleva {b['steps']} pasos hoy{modo}."

    if "recuérdame" in t or "recuerdame" in t or "recordar" in t or "hora de" in t:
        bridge.enviar_comando("remind")  # vibra el wearable
        return "Le avisé con una vibración."

    return "No entendí. Prueba: 'que es esto', 'esto es mi celular', 'estoy en la sala', 'donde esta mi celular'."


def monitor_biometricos():
    """Emite biométricos periódicos y escala alertas (SOS / caída) al backend."""
    import time

    while True:
        b = bridge.biometricos()
        if not b.get("stub"):
            cloud.emitir("biometrico", {"hr": b["hr"], "steps": b["steps"], "act": b["act"]})
            if b.get("sos"):
                cloud.emitir("alerta", {"motivo": "SOS", "hr": b["hr"]})
            if b.get("fall"):
                cloud.emitir("alerta", {"motivo": "posible caida"})
        time.sleep(3)


def main():
    import threading

    bridge.iniciar()  # abre el puente MCU (o queda en stub)
    threading.Thread(target=monitor_biometricos, daemon=True).start()
    print(f"[Uno Q] modo={config.MODE} online={config.online()}")
    print("Asistente de entorno listo. Escribe 'salir' para terminar.")
    while True:
        try:
            texto = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if texto.lower() in {"salir", "exit", "quit"}:
            break
        print(procesar(texto))


if __name__ == "__main__":
    main()
