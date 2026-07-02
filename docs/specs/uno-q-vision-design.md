# Diseño — Módulo de visión y memoria espacial en Arduino Uno Q

> Fecha: 2026-07-02. El Arduino Uno Q (2GB) fue prestado → las smart glasses / visión suben de
> Capa C (roadmap) a **Capa A (demo real)**. Este módulo corre en el lado Linux (Debian) del Uno Q.

## 1. Qué demuestra (prioridad de wow)

1. **"¿Qué es esto?"** — detección de objetos on-device (TFLite COCO SSD) → nombra el objeto.
2. **"Mis objetos"** — el usuario etiqueta un objeto genérico como suyo ("esto es mi celular") →
   luego lo nombra como "tu celular".
3. **⭐ Memoria espacial aumentada** — registra dónde vio cada objeto por última vez; "¿dónde dejé
   mi celular?" → "lo vi en la mesa gris hace 20 minutos". Es la idea casi inédita de los docs
   (§6.7 Hackathon_Master). Futuro: reforzar con AirTag/UWB.
4. **Reconocimiento facial** — enrola caras conocidas → "te está hablando Sofía, tu nieta".
5. **Asistente de voz paralelo** — altavoz siempre-con-el-paciente; online usa Gemini (reusa el
   backend `/chat`), offline responde local. Comparte funciones con la app del celular.

## 2. Doble modo (edge ↔ cloud)

| Modo | Cuándo | Qué hace |
|---|---|---|
| **edge** | Sin red / privacidad | Visión + memoria + STT/TTS local; todo en SQLite local del Uno Q |
| **cloud** | Con red | Además: LLM Gemini para conversación, sincroniza eventos al backend (Gemelo/PKG) |
| **auto** | Por defecto | Detecta conectividad; degrada a edge si no hay red |

Config por `MODE` en `uno_q/config.py`. La visión y la memoria espacial SIEMPRE corren local
(privacidad: la voz e imagen son biométricos, no se suben crudas — solo *eventos*).

## 3. Arquitectura del módulo

```
uno_q/
  config.py            MODE, backend URL, rutas de modelos
  vision/
    detector.py        objeto: TFLite COCO SSD (90 clases) + "qué es esto"
    faces.py           enrolar + reconocer (OpenCV LBPH, sin dlib → liviano en ARM)
    my_objects.py      mapea clase genérica -> etiqueta personal ("tu celular")
    spatial_memory.py  SQLite: último avistamiento por objeto + zona + tiempo
  voice/assistant.py   mic -> STT (online Gemini / offline vosk) -> TTS -> altavoz
  sync/cloud.py        empuja eventos al backend cuando hay red; cola offline
  app.py               loop principal (dev: CLI+webcam; device: voz+cámara)
  models/              coco_ssd_mobilenet.tflite + labels.txt (descargar)
```

## 4. Elecciones técnicas (pragmáticas para A53 + 2 días)

- **Objetos:** TFLite COCO SSD MobileNet v1 (90 clases, incluye celular/taza/llaves) — liviano,
  captura on-demand (no video en tiempo real). Alternativa: modelo FOMO entrenado en Edge Impulse
  y exportado a TFLite/Linux (para "mis objetos" específicos).
- **Caras:** OpenCV LBPH (`opencv-contrib-python`) — no requiere dlib, entrena con pocas fotos.
- **STT offline:** vosk (modelo español pequeño). **Online:** Gemini / Google STT.
- **TTS:** offline piper/espeak-ng; online gTTS/Gemini.
- **Cámara:** USB webcam (más confiable que el conector nativo). Dev en laptop con webcam.
- **Integración backend:** nuevo endpoint `POST /vision/ingest` guarda eventos de visión como
  `Event` y alimenta el PKG/Gemelo. Offline se encolan y se envían al reconectar.

## 5. Ejecución en el Uno Q (dos caminos)

- **Standalone:** SSH al Debian del Uno Q → `python uno_q/app.py` (portátil, no depende de App Lab).
- **Arduino App Lab 0.8.0:** envolver `app.py` como "app" de Python (Bricks) + sketch MCU para
  botón/LED. Los modelos se pueden entrenar/exportar desde Edge Impulse dentro de App Lab.

El software se desarrolla y prueba en laptop con webcam; se copia al Uno Q para la demo. Degrada a
stub si falta cámara o modelo (para no bloquear el desarrollo).

## 6. Alcance realista (2 días)

- ✅ Objetos + "qué es esto" + "mis objetos" + memoria espacial (núcleo del wow).
- ✅ Reconocimiento facial básico (enrolar 1-2 caras del equipo).
- 🔶 Voz: loop funcional online (Gemini); offline vosk/piper si sobra tiempo.
- 🔶 Sync backend: endpoint + envío online; cola offline si sobra tiempo.
- 🔷 NPU Qualcomm (SNPE/QNN), SLAM 3D, AirTag/UWB → roadmap.
