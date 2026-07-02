"""Reconocimiento facial ligero (OpenCV LBPH, sin dlib → corre bien en ARM/A53).

Enrola caras conocidas (familia, cuidador, el propio paciente) y las reconoce → "te habla Sofía".
Degrada a stub si falta opencv-contrib (módulo face) o el cascade.
"""
import json

from uno_q import config

_recognizer = None
_labels: dict[int, str] = {}


def _cascade():
    import cv2

    path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    return cv2.CascadeClassifier(path)


def _detectar_caras(gray):
    return _cascade().detectMultiScale(gray, 1.1, 5, minSize=(60, 60))


def enrolar(nombre: str, frames: list) -> dict:
    """Entrena/re-entrena con una lista de frames BGR que contienen la cara de `nombre`."""
    try:
        import cv2
        import numpy as np
    except Exception:
        return {"error": "opencv no disponible"}

    global _recognizer, _labels
    _cargar()
    # asignar id al nombre
    ids = {v: k for k, v in _labels.items()}
    fid = ids.get(nombre, (max(_labels) + 1) if _labels else 0)
    _labels[fid] = nombre

    caras, etiquetas = [], []
    for f in frames:
        gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in _detectar_caras(gray):
            caras.append(cv2.resize(gray[y:y + h, x:x + w], (200, 200)))
            etiquetas.append(fid)
    if not caras:
        return {"error": "no se detectó ninguna cara en los frames"}

    if _recognizer is None:
        _recognizer = cv2.face.LBPHFaceRecognizer_create()
        _recognizer.train(caras, np.array(etiquetas))
    else:
        _recognizer.update(caras, np.array(etiquetas))
    _recognizer.write(str(config.FACE_MODEL))
    config.FACE_LABELS.write_text(json.dumps(_labels), encoding="utf-8")
    return {"ok": True, "nombre": nombre, "muestras": len(caras)}


def _cargar() -> bool:
    global _recognizer, _labels
    if not config.FACE_MODEL.exists():
        return False
    try:
        import cv2

        _recognizer = cv2.face.LBPHFaceRecognizer_create()
        _recognizer.read(str(config.FACE_MODEL))
        _labels = {int(k): v for k, v in json.loads(config.FACE_LABELS.read_text()).items()}
        return True
    except Exception:
        return False


def reconocer(frame) -> str:
    """Devuelve el nombre de la persona reconocida o 'alguien que no reconozco'."""
    if frame is None or not _cargar():
        return "alguien que no reconozco"
    try:
        import cv2

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in _detectar_caras(gray):
            cara = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            fid, dist = _recognizer.predict(cara)
            if dist < 70:  # umbral LBPH (menor = más seguro)
                return _labels.get(fid, "alguien que no reconozco")
    except Exception:
        pass
    return "alguien que no reconozco"
