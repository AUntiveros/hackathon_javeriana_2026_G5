"""Detección de objetos on-device (TFLite COCO SSD MobileNet).

Degrada a stub si faltan tflite/opencv o el modelo, para no bloquear el desarrollo.
Descarga del modelo: ver uno_q/README.md.
"""
from uno_q import config

_interpreter = None
_labels = None


def _load():
    global _interpreter, _labels
    if _interpreter is not None:
        return True
    if not config.OBJ_MODEL.exists():
        return False
    try:
        try:
            from tflite_runtime.interpreter import Interpreter
        except Exception:
            from tensorflow.lite import Interpreter  # type: ignore
        _interpreter = Interpreter(model_path=str(config.OBJ_MODEL))
        _interpreter.allocate_tensors()
        _labels = config.OBJ_LABELS.read_text(encoding="utf-8").splitlines()
        return True
    except Exception:
        return False


def detectar(frame) -> list[dict]:
    """frame = imagen BGR (numpy) o None. Devuelve [{label, score, bbox}] ordenado por score."""
    if frame is None or not _load():
        return _stub()
    import numpy as np

    inp = _interpreter.get_input_details()[0]
    _, h, w, _ = inp["shape"]
    try:
        import cv2

        img = cv2.resize(frame, (w, h))
    except Exception:
        return _stub()
    data = np.expand_dims(img, 0).astype(np.uint8 if inp["dtype"] == np.uint8 else np.float32)
    _interpreter.set_tensor(inp["index"], data)
    _interpreter.invoke()
    out = _interpreter.get_output_details()
    boxes = _interpreter.get_tensor(out[0]["index"])[0]
    classes = _interpreter.get_tensor(out[1]["index"])[0]
    scores = _interpreter.get_tensor(out[2]["index"])[0]

    res = []
    for i in range(len(scores)):
        if scores[i] < config.DET_SCORE_MIN:
            continue
        idx = int(classes[i])
        label = _labels[idx] if 0 <= idx < len(_labels) else str(idx)
        res.append({"label": label, "score": float(scores[i]), "bbox": boxes[i].tolist()})
    res.sort(key=lambda r: -r["score"])
    return res or _stub()


def _stub() -> list[dict]:
    """Sin modelo/cámara: devuelve una detección simulada para probar el flujo."""
    return [{"label": "cell phone", "score": 0.0, "bbox": [0, 0, 1, 1], "stub": True}]


def capturar(source=0):
    """Captura un frame de la webcam. Devuelve None si no hay cámara."""
    try:
        import cv2

        cap = cv2.VideoCapture(source)
        ok, frame = cap.read()
        cap.release()
        return frame if ok else None
    except Exception:
        return None
