# Asistente de entorno — Arduino Uno Q (visión + memoria espacial)

Corre en el lado **Linux (Debian)** del Uno Q. Se desarrolla y prueba en laptop con webcam, luego
se copia al Uno Q. Diseño completo en `docs/specs/uno-q-vision-design.md`.

## Qué hace
- **"¿Qué es esto?"** → detección de objetos (TFLite COCO SSD).
- **"Esto es mi celular"** → etiqueta personal ("tu celular").
- **⭐ Memoria espacial** → "¿dónde dejé mi celular?" → "en la mesa gris hace 20 min".
- (fase siguiente) reconocimiento facial, voz online/offline, sync con backend.

## Probar YA en laptop (sin cámara → modo stub)
```bash
pip install opencv-contrib-python numpy pillow requests
python -m uno_q.app
# > estoy en la mesa gris
# > esto es mi celular
# > que es esto
# > donde esta mi celular
```
Sin modelo/cámara usa una detección simulada (cell phone) para validar el flujo. Con webcam +
modelo detecta de verdad.

## Descargar el modelo de objetos
Colocar en `uno_q/models/`:
- `coco_ssd_mobilenet.tflite` — SSD MobileNet v1 COCO (90 clases, cuantizado uint8).
  Fuente: TensorFlow Hub / coral.ai models ("ssd_mobilenet_v1_1_metadata_1.tflite" o el detector
  COCO de Coral). Renombrar a `coco_ssd_mobilenet.tflite`.
- `labels.txt` — una etiqueta COCO por línea (0='person' … incluye 'cell phone', 'cup', 'keys'…).

Instalar runtime ligero (en el Uno Q / Linux):
```bash
pip install tflite-runtime
```
En Windows dev, si no hay `tflite-runtime`, el módulo cae a stub (o instala `tensorflow`, pesado).

## Desplegar en el Uno Q
**Camino A — standalone (recomendado, no depende de App Lab):**
1. Conectar USB webcam al Uno Q (más confiable que el conector nativo de cámara).
2. SSH al Debian del Uno Q. Copiar la carpeta `uno_q/`.
3. `pip install -r uno_q/requirements.txt` (+ `tflite-runtime`).
4. `python -m uno_q.app`. Cablear a voz en la fase siguiente (`voice/assistant.py`).

**Camino B — Arduino App Lab 0.8.0:**
- Crear una "app" de Python que llame a `app.procesar()`; el sketch del MCU maneja botón/LED de
  captura. Modelos personalizados ("mis objetos" específicos): entrenar un **FOMO** en Edge
  Impulse, exportar a TFLite/Linux y apuntar `config.OBJ_MODEL` a ese archivo.

## Modo edge ↔ cloud
`UNOQ_MODE=edge|cloud|auto` (default auto). Edge: todo local (privacidad; voz/imagen no salen,
solo eventos). Cloud: además LLM Gemini + sync al backend. La visión y la memoria espacial SIEMPRE
corren local.

## Construido y probado (flujo con stub)
- `vision/detector.py` — objetos TFLite (stub sin modelo).
- `vision/my_objects.py` — etiquetas personales.
- `vision/spatial_memory.py` — memoria espacial (el wow).
- `vision/faces.py` — enrolar/reconocer caras (OpenCV LBPH).
- `voice/assistant.py` — altavoz paralelo: comandos de visión local + conversación al backend `/chat`.
- `sync/cloud.py` + backend `POST /vision/ingest` — alimenta la DB del asistente con lo que ve.

## Pendiente (necesita el hardware físico)
- Descargar `coco_ssd_mobilenet.tflite` + `labels.txt` a `models/` y `pip install tflite-runtime`.
- Conectar USB webcam + micrófono al Uno Q; enrolar 1-2 caras del equipo (`faces.enrolar`).
- Offline STT: bajar modelo vosk-es pequeño; TTS offline: `espeak-ng` (o piper).
- Correr `python -m uno_q.voice.assistant` en el Uno Q.
