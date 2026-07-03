# 🎼 Nino — Ecosistema de Inteligencia Aumentada para Alzheimer

> **"La IA es el director de orquesta de la red de cuidado, no el solista."**

Solución integral para el cuidado y tratamiento de personas con Alzheimer, mediada por IA, que orquesta la relación entre **paciente**, **cuidador**, **médico**, **familiar** y **comunidad**. Desarrollado en la Hackathon Javeriana 2026 — Cuidado del Adulto Mayor desde la Biomédica y Tecnologías Emergentes.

---

> ## ⚠️ PIVOTE 2026-07-03 — leer antes que el resto de este README
> El hackathon **delimitó** el problema a **recordatorios de una rutina cotidiana** (confirmar si se
> hizo + avisar al cuidador si no) y **prohibió** diagnosticar/monitorear deterioro cognitivo y el
> prototipo de cámara. Por eso:
> - **Descartado → `backup/`**: biomarcadores de voz (`ml/`) y visión Uno Q (cámara). Ver `backup/README.md`.
> - **Nuevo centro**: asistente-guía de rutina con **motor de criticidad (lógica difusa)** que respeta la autonomía (no fuerza).
> - **Documentación viva y correcta**: `docs/investigacion/` (estadísticas, mapas de empatía, estado del arte) y `docs/plan/plan-ejecucion-v2.md`.
> - Las tablas de estado de abajo son **previas al pivote** (referencia histórica); el estado vigente está en el plan v2.

---

## 🧠 ¿Qué es Nino?

Nino es un ecosistema de IA que **no reemplaza** las relaciones humanas del paciente con Alzheimer, sino que las **amplifica y orquesta**. A través de un chatbot multi-agente con roles diferenciados (RBAC), biomarcadores de voz, un Gemelo Cognitivo Digital y hardware asistivo, Nino:

- 🧓 **Para el paciente**: Compañero empático del día a día, aprende su historia personal (PKG/Digital Twin), genera conversaciones de reminiscencia terapéutica, le recuerda cosas puntuales, y monitorea su progresión cognitiva a través de biomarcadores de voz.
- 🤝 **Para el cuidador**: Gestiona medicamentos, agenda actividades no repetitivas, comparte ubicación, media conversaciones, recuerda citas médicas y ofrece apoyo empático.
- 🩺 **Para el médico**: Envía reportes de progresión, señales clínicas del habla, registros longitudinales, gestiona terapias y permite monitoreo de adherencia farmacológica.
- 👨‍👩‍👧 **Para los familiares**: Fomenta llamadas, propone temas de conversación de interés, conecta emocionalmente con el paciente.
- 🏘️ **Para la comunidad**: Orquesta redes de apoyo, conecta con pares, genera actividades grupales.

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND (React 19 + Vite 8)               │
│   Voice-first PWA · 5 vistas por rol (RBAC) + Dashboard     │
│   Nino (mascota SVG animada) · Web Speech API · Web BLE     │
│   [/paciente → fullscreen] [/ → equipo de cuidado]           │
└──────────────┬─────────────────────────┬────────────────────┘
               │ REST / mock dual-mode    │ BLE (Web Bluetooth)
               ▼                          ▼
┌──────────────────────────────┐  ┌───────────────────────────┐
│   BACKEND API (FastAPI)       │  │   HARDWARE                 │
│                               │  │                            │
│  ┌─────────────────────────┐  │  │  Arduino Uno Q (primario)  │
│  │ ORQUESTADOR (5 agentes) │  │  │   Linux: visión + voz +    │
│  │  Role Router = RBAC     │  │  │     memoria espacial       │
│  │  + Guardrails + Memory  │  │  │   MCU: FC + pasos + SOS    │
│  └────────┬────────┬───────┘  │  │     + vibración (serial)   │
│           │        │          │  │                            │
│   ┌───────┘  ┌─────┘         │  │  ESP32 (alternativa BLE)   │
│   ▼          ▼               │  └───────────────────────────┘
│  RAG       SES              │
│ (Chroma)  (Personalizer)    │──────▶ Gemini 2.5 Flash (LLM)
│   │                          │
│   ▼                          │
│  Motor de Rutina             │
│  (anti-repetición + alertas) │
│   │                          │
│   ▼                          │
│  Pipeline Biomarcadores      │  ← Whisper + librosa + spaCy-es
│  (voz → features → riesgo)  │    + XGBoost/RF/SVM
│   │                          │
│   ▼                          │
│  DB (SQLite)                 │
│  Patient · Event · Biomarker │
│  · TwinSnapshot              │
└──────────────────────────────┘
```

### Diagramas detallados

Ver [docs/diagrams/arquitectura.md](docs/diagrams/arquitectura.md) — incluye 7 diagramas Mermaid: C4 Contexto, C4 Contenedores, C4 Componentes del Orquestador, Loop biomarcadores, Orquestación día-a-día (secuencia), Máquina de estados ESP32, y Despliegue.

---

## 📊 Estado de Implementación

### ✅ Completado (Capa A — se construye)

| Módulo | Archivos | Estado | Detalles |
|--------|----------|--------|----------|
| **Backend API** | 17 .py + DB + seed | ✅ MVP funcional | 10 endpoints, CORS, Pydantic models |
| **Orquestador RBAC** | 4 archivos | ✅ Completo | 5 roles con system prompts, tools, scope, guardrails |
| **RAG (PKG Don José)** | 3 archivos + ChromaDB | ✅ Ingestado y probado | Gemini embeddings + fallback sentence-transformers |
| **Motor de Rutina** | 1 archivo | ✅ Completo | 7 actividades culturalmente relevantes, anti-repetición, alertas |
| **SES Personalizer** | 1 archivo | ✅ Completo | Reserva cognitiva, ajuste de riesgo, perfil para prompt |
| **Pipeline Biomarcadores** | 2 archivos + model.pkl | ⚠️ Funcional (heurístico) | `_extract_real()` es stub; modelo carga si existe pkl |
| **Frontend** | 42 archivos | ✅ **Todo completo** | PWA dual (paciente fullscreen + equipo), Nino animado, 5 vistas, mock-first |
| **ML Pipeline** | 12 archivos + model.pkl | ✅ Completo (datos sintéticos) | 6 pasos, fairness, model card. Dataset real pendiente |
| **Uno Q — Visión** | 18 archivos | ✅ Probado en stub | Detección objetos, memoria espacial ⭐, objetos personales, facial |
| **Uno Q — MCU** | 1 firmware | ✅ Completo | FC + pasos + SOS + vibración vía serial bridge |
| **ESP32 Wearable** | 3 archivos | ✅ Completo | Firmware BLE + página test Web Bluetooth |
| **Documentación** | 10 archivos | ✅ Exhaustiva | Specs, C4, plan atómico, hardware guide, API guide |
| **Investigación** | 4 documentos (120K+) | ✅ Completa | Revisión sistemática + 3 revisiones de estado del arte |

### ⚠️ Pendiente / En progreso

| Ítem | Prioridad | Qué falta |
|------|-----------|-----------|
| `biomarkers/extract._extract_real()` | P1 | Conectar Whisper + librosa + parselmouth + spaCy al pipeline real |
| Dataset real (MultiConAD/Ivanova) | P1 | MultiConAD no disponible en HF; Ivanova requiere membresía DementiaBank |
| STT en Uno Q (`voice/assistant.py`) | P2 | Integrar vosk o Gemini STT (usa input texto como fallback) |
| Descargar modelo TFLite COCO SSD | P2 | Archivo `models/coco_ssd_mobilenet.tflite` falta en disco |
| Enrolar caras conocidas | P2 | Faces LBPH implementado pero sin datos de entrenamiento |
| Conectar frontend ↔ backend real | P2 | Solo cambiar `VITE_API_URL` en .env del frontend |
| Vistas Familiar/Comunidad con API | P3 | Datos hardcodeados, sin endpoints backend para estos roles |

### 🔶 Capa B — Se mockea (demo visual convincente)

- Panel médico con señales clínicas del habla ("subió 25% repetición de preguntas") — **ya implementado con datos mock**
- Orquestación red humana ("hoy llama a tu nieta Sofía") — **implementado en vista Familiar con datos hardcoded**
- Ubicación en tiempo real / geofence del paciente — **slide/roadmap**

### 🔷 Capa C — Roadmap (solo slides + papers de respaldo)

- Smart glasses con visión ("¿qué estoy viendo?", reconocimiento facial) — **código existe en `uno_q/`, pendiente hardware físico**
- Smart home IoT, cámara ambiental, sensores biomédicos extra
- Social/Home Digital Twin completo
- Federated Learning, Edge AI avanzado, NPU/SLAM/UWB

---

## 🚀 Quick Start

### Backend

```bash
cd "D:/UNIDAD D/UNIVERSIDAD/2026-1/Hackathon Javeriana"
python -m venv .venv && .venv/Scripts/activate         # Windows
pip install -r backend/requirements.txt
python -m spacy download es_core_news_lg               # para biomarcadores
cp backend/.env.example backend/.env                   # pegar GEMINI_API_KEY

python -m backend.db.seed                              # puebla Don José + 30 días
python -m backend.rag.ingest                           # carga PKG a ChromaDB
uvicorn backend.main:app --reload                      # http://localhost:8000/docs
```

**Endpoints disponibles:**
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/chat` | Chat RBAC `{rol, mensaje, patient_id}` |
| GET | `/patients/{id}` | Datos del paciente |
| GET | `/routine/{id}/today` | Agenda del día |
| GET | `/twin/{id}/trend` | Tendencia cognitiva (30 días) |
| GET | `/twin/{id}/snapshot` | Snapshot del Gemelo Cognitivo |
| POST | `/biomarkers/analyze` | Análisis de biomarcadores de voz |
| POST | `/vision/ingest` | Ingestar evento de visión (Uno Q) |
| GET | `/vision/{id}/recent` | Eventos recientes de visión |
| GET | `/ses/{id}/riesgo` | Perfil de riesgo SES |

> Sin `GEMINI_API_KEY`, el chat corre en modo offline (contexto/scope sin LLM). RAG funciona con `sentence-transformers`.

### Frontend

```bash
cd frontend
npm install
npm run dev                                            # http://localhost:5173
```

- **`/`** → App del equipo de cuidado (selector de rol: cuidador, médico, familiar, comunidad)
- **`/paciente`** → App del paciente (fullscreen, voice-first, mascota Nino)

> Funciona 100% standalone con datos mock. Para conectar al backend: `VITE_API_URL=http://localhost:8000` en `.env`.

### ML Pipeline

```bash
cd ml
pip install -r requirements.txt
python 00_download.py    # descarga/sintetiza datos
python 01_features.py    # extrae features
python 02_baseline.py    # modelo baseline P(AD|Voz)
python 03_ses_model.py   # modelo +SES P(AD|Voz,SES)
python 04_fairness.py    # análisis de equidad por educación
python 05_export.py      # exporta model.pkl + model_card.md
```

### Hardware — Arduino Uno Q

```bash
cd uno_q
pip install -r requirements.txt
python app.py                                          # modo stub (sin cámara/serial)
# Comandos: "ver", "esto es mi celular", "donde esta mi celular", "signos"
```

### Hardware — ESP32 (alternativa)

Cargar `hardware/esp32/esp32_wearable/esp32_wearable.ino` en Arduino IDE. Probar con `hardware/esp32/test_webbluetooth.html` en Chrome.

---

## 🔬 Diferenciadores vs Estado del Arte

### Lo que nadie más tiene (White Space)

| # | Diferenciador | Por qué importa | Evidencia |
|---|--------------|------------------|-----------|
| 1 | **P(AD\|Voz, Contexto SES) vs P(AD\|Voz)** | Los modelos actuales confunden baja educación con deterioro cognitivo → falsos positivos en poblaciones vulnerables. Nuestro pipeline ajusta por reserva cognitiva (educación, IDH, bilingüismo, profesión). | **Nadie ha medido el delta AUC estratificado por nivel educativo en español.** Es publicable. |
| 2 | **Orquestación de red humana, no reemplazo** | La IA no conversa "en vez de" la familia; genera las conversaciones humanas ("hoy llama a tu nieta Sofía y pregúntale por su gato"). | Concepto Human-Augmented AI: la IA desaparece cuando la conexión humana funciona. |
| 3 | **Memoria espacial aumentada** ⭐ | "¿Dónde dejé mi celular?" → "Lo vi en la mesa gris hace 20 minutos". SLAM + visual memory para objetos del paciente. | Casi sin precedente en la literatura para Alzheimer. |
| 4 | **RBAC agéntico con 5 roles** | Cada actor (paciente/cuidador/médico/familiar/comunidad) ve datos diferentes, con tono diferente, y herramientas diferentes. Un solo chatbot, 5 experiencias. | Los asistentes existentes son para un solo usuario. |
| 5 | **Español + contexto LATAM + Quechua** | Modelos de habla evaluados en inglés; datasets en español escasos. El paciente semilla (Don José, Cusco, quechua-español, primaria incompleta) valida el impacto en poblaciones subrepresentadas. | Nicho no cubierto. |
| 6 | **Conversación como fuente de biomarcadores** | La misma conversación terapéutica (reminiscencia, CST) es la que genera los datos para el pipeline de detección. No hay "sesión de test" separada. | Loop cerrado: terapia → datos → personalización → mejor terapia. |

### Benchmarking de mercado

| Producto | Qué hace | Qué NO hace (y Nino sí) |
|----------|----------|--------------------------|
| CareYaya MedaCareLLM | Chatbot para cuidadores | No tiene RBAC multi-rol, no monitorea voz, no hardware |
| CrossSense "Wispy" | Detección AD por voz (Longitude Prize) | Solo detección, no terapia ni orquestación de red |
| Moneta Health | Conversación terapéutica (n=75 RCT) | Solo paciente, no integra cuidador/médico/familia |
| Ray-Ban Meta | Smart glasses con IA | No personalizado para Alzheimer, no edge offline |
| PARO robot | Companion robot (mejor evidencia RCT) | Hardware caro, no escala, no conecta red humana |

---

## 📁 Estructura del Proyecto

```
hackathon-javeriana/
├── backend/                          # FastAPI + Orquestador + RAG + Biomarcadores
│   ├── main.py                       # 10 endpoints REST
│   ├── orchestrator/                 # RBAC: agents, router, tools, guardrails
│   ├── rag/                          # ChromaDB: ingest, retriever, demo_chat
│   ├── biomarkers/                   # extract (stub real) + predict (heurístico/pkl)
│   ├── routine/                      # Motor de rutina diaria anti-repetición
│   ├── ses/                          # Personalizer SES + reserva cognitiva
│   ├── db/                           # SQLModel: Patient, Event, Biomarker, TwinSnapshot
│   ├── seed/                         # don_jose.json (PKG semilla)
│   ├── app.db                        # SQLite pre-poblada (30 días)
│   └── chroma_db/                    # Vector store ingestado
│
├── frontend/                         # React 19 + Vite 8 + TypeScript
│   ├── src/
│   │   ├── apps/                     # PacienteApp (voice-first) + EquipoApp (roles)
│   │   ├── components/               # Nino (mascota SVG), TwinDashboard, WearablePanel
│   │   ├── views/                    # CuidadorView, MedicoView, FamiliarView, ComunidadView
│   │   ├── hooks/                    # useAcompanante, useWearable, useVoz
│   │   └── api/                      # client (dual mock/real), types, mock data
│   └── public/                       # PWA manifests, SW, icons
│
├── ml/                               # Pipeline de biomarcadores de voz
│   ├── 00_download.py → 05_export.py # Pipeline secuencial completo
│   ├── common.py                     # Features + síntesis de datos
│   ├── modeling.py                   # XGBoost/RF/SVM + CV
│   ├── model.pkl                     # Modelo entrenado (datos sintéticos)
│   ├── feature_schema.json           # Contrato de features con backend
│   └── model_card.md                 # Model card con métricas + limitaciones
│
├── uno_q/                            # Asistente ambiental (Arduino Uno Q)
│   ├── app.py                        # Loop principal de comandos
│   ├── vision/                       # detector, faces, my_objects, spatial_memory ⭐
│   ├── voice/                        # assistant (TTS/STT + chatbot)
│   ├── hardware/                     # bridge serial Linux↔MCU
│   ├── sync/                         # cloud sync online/offline
│   └── data/                         # spatial_memory.db, my_objects.json
│
├── hardware/
│   ├── esp32/                        # Firmware BLE + test Web Bluetooth
│   └── unoq_mcu/                    # Firmware MCU (biométricos vía serial)
│
├── docs/
│   ├── specs/                        # Design spec + Uno Q vision spec
│   ├── diagrams/                     # 7 diagramas Mermaid (C4 + flujos)
│   ├── plan/                         # Implementation plan + PROMPT de entrenamiento ML
│   ├── setup/                        # Guía Gemini API key
│   └── hardware/                     # BOM, pinout, guía hardware, lista de compra
│
├── revisiones puntuales/             # 3 revisiones de estado del arte
├── Hackathon_Master.md               # Documento maestro (537 líneas, visión completa)
└── Revision_Sistematica_*.md         # Revisión sistemática 2023-2026 (440 líneas)
```

---

## 🛠️ Stack Técnico

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| LLM | Gemini 2.5 Flash | Function-calling nativo, tier gratis generoso, rápido |
| Backend | FastAPI + SQLModel + SQLite | Ligero, async, ORM tipado |
| RAG | ChromaDB + Gemini `text-embedding-004` | Vector store embebido; fallback `sentence-transformers` |
| Frontend | React 19 + Vite 8 + recharts | PWA voice-first, Web Speech API, Web Bluetooth |
| STT/TTS | Web Speech API (navegador) / Whisper (pipeline) | Cero costo en navegador; Whisper para biomarcadores |
| Features acústicas | librosa + praat-parselmouth | MFCC, F0, jitter, shimmer, HNR |
| Features lingüísticas | spaCy `es_core_news_lg` | TTR, MATTR, Brunet, Honoré, complejidad |
| Clasificador | XGBoost / RandomForest / SVM | Rápido, interpretable, compara baseline vs +SES |
| Hardware primario | Arduino Uno Q (Linux + MCU) | Visión edge + biométricos en un solo dispositivo |
| Hardware alternativo | ESP32 + MAX30102 + MPU6050 | Wearable BLE roadmap |
| Sensores | MAX30102 (FC/SpO2) + MPU6050 (acelerómetro/giroscopio) | Signos vitales + detección caídas + conteo pasos |

---

## 👥 Equipo (5 personas)

| Rol | Responsabilidad | Tracks |
|-----|----------------|--------|
| **Alvaro** (Full-stack + IA + HW) | Orquestador, backend, IA/RAG, biomarcadores, hardware, integración | Backend, ML, Hardware |
| **Frontend** | React/Vite, vistas por rol, dashboard Gemelo, BLE | Frontend |
| **Contacto-paciente** | Scripts terapéuticos, PKG semilla, entrevistas, pitch | Contenido |
| **Diseño** | Identidad visual, mockups Capa B/C, video, slides | Diseño |
| **Flexible** | Datos (MultiConAD), baseline, QA, documentación | ML, QA |

---

## 📚 Documentación de Referencia

| Documento | Contenido | Líneas |
|-----------|-----------|--------|
| [Hackathon_Master.md](Hackathon_Master.md) | Visión completa, filosofía, 14 secciones, catálogo de papers | 537 |
| [Revisión Sistemática](Revision_Sistematica_Asistentes_IA_Alzheimer_2023-2026.md) | Estado del arte 2023-2026, 15 papers detallados, gaps | 440 |
| [Spec de diseño](docs/specs/2026-07-02-ecosistema-alzheimer-design.md) | Arquitectura C4, stack, RBAC matrix, ética, riesgos | 118 |
| [Spec Uno Q Vision](docs/specs/uno-q-vision-design.md) | Módulo de visión + memoria espacial, diseño dual edge/cloud | 73 |
| [Plan de implementación](docs/plan/implementation-plan.md) | Tareas atómicas por track, schedule 2 días | 150 |
| [PROMPT entrenamiento ML](docs/plan/PROMPT-entrenamiento.md) | Prompt listo para terminal paralela → entrena modelo | 114 |
| [Guía Gemini API](docs/setup/gemini-api-guide.md) | Obtener key, .env, smoke test, límites, fallback | 59 |
| [Guía Hardware](docs/hardware/hardware-guide.md) | BOM ESP32, pinout, firmware, ruta Uno Q | 72 |
| [Lista de compra](docs/hardware/lista-compra.md) | BOM actualizado (consolidado en Uno Q) | 67 |
| [Estrategia Perú](revisiones%20puntuales/Estrategia%20nacional%20de%20investigación%20para%20el%20diagnóstico%20de%20la%20enfermedad%20de%20Alzheimer%20mediante%20el%20análisis%20computacional%20del%20habla%20en%20el%20Perú%20(Abril%202026).md) | Estrategia nacional, datasets, contactos | 114 |
| [Integración SES](revisiones%20puntuales/Integración%20de%20Datos%20Socioeconómicos%20en%20Modelos.md) | SES en modelos neurodegenerativos, fairness ML | 184 |
| [Validación Modelos Habla](revisiones%20puntuales/Investigación%20Alzheimer_%20Validación%20Modelos%20Habla.md) | Validación cross-lingual, transfer learning, publicación Q1 | 192 |

---

## 🎯 Métricas del Prototipo (datos sintéticos)

| Métrica | Baseline P(AD\|Voz) | +SES P(AD\|Voz,SES) | Delta |
|---------|---------------------|---------------------|-------|
| AUC | 0.746 | 0.750 | +0.004 |
| FPR grupo baja educación | 0.41 | 0.27 | **-34%** ⭐ |

> **El resultado clave**: la calibración por SES reduce los falsos positivos en poblaciones de baja educación en un 34%, sin sacrificar sensibilidad. Con datos reales (Ivanova/MultiConAD), este delta será el hallazgo publicable.

---

## 📄 Licencia

Prototipo de hackathon — uso académico.

---

*Hackathon Javeriana 2026 · Grupo 5 · Ingeniería Biomédica × Tecnologías Emergentes*
