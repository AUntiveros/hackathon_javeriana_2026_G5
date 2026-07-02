# Plan de implementación troceado — para modelo ligero (Sonnet)

> Cada tarea es atómica y autocontenida. Un modelo sin contexto del proyecto puede ejecutarla leyendo solo:
> el spec (`docs/specs/2026-07-02-ecosistema-alzheimer-design.md`) + la tarea.
> Formato por tarea: **objetivo · archivos · dependencias · pasos · criterio de HECHO**.
> Prioridad: P0 = imprescindible para demo, P1 = importante, P2 = si sobra tiempo.

## Estructura de repo objetivo

```
/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── orchestrator/
│   │   ├── router.py           # RBAC role router
│   │   ├── agents.py           # 5 role agents
│   │   ├── tools.py            # function-calling tools
│   │   ├── guardrails.py       # anti-alucinación
│   │   └── memory.py           # memory manager por rol
│   ├── rag/
│   │   ├── ingest.py           # carga PKG a ChromaDB
│   │   └── retriever.py
│   ├── routine/engine.py       # orquestación día-a-día
│   ├── biomarkers/
│   │   ├── extract.py          # Whisper + features
│   │   └── predict.py          # carga modelo.pkl, infiere
│   ├── ses/personalizer.py
│   ├── db/models.py            # SQLModel
│   └── seed/don_jose.json      # PKG semilla
├── frontend/                   # React + Vite
├── ml/                         # entrenamiento (track paralelo)
├── hardware/esp32/             # firmware
└── docs/
```

---

## TRACK BACKEND (Alvaro)

### T1 [P0] Scaffold FastAPI + DB
- **Archivos:** `backend/main.py`, `backend/db/models.py`, `backend/requirements.txt`
- **Deps:** ninguna
- **Pasos:** FastAPI app con CORS abierto. SQLModel con tablas Patient, Event, Biomarker, TwinSnapshot (schema en spec §5). Endpoint `GET /health`.
- **HECHO:** `uvicorn backend.main:app` levanta; `/health` responde 200.

### T2 [P0] Seed PKG "Don José"
- **Archivos:** `backend/seed/don_jose.json`, `backend/db/seed.py`
- **Deps:** T1
- **Pasos:** Persona ficticia: 78 años, ex-agricultor, escolaridad primaria, zona rural, quechua-español. Familia (esposa María †, hija Rosa, nieta Sofía, bisnieto). Rutina base, intereses (fútbol, música criolla, su chacra), 30 días de biomarcadores simulados con tendencia leve de deterioro. **Este perfil valida la historia de impacto (baja escolaridad mal clasificada).**
- **HECHO:** `seed.py` puebla la DB; `GET /patients/1` devuelve a Don José.

### T3 [P0] RAG — ingest PKG a ChromaDB
- **Archivos:** `backend/rag/ingest.py`, `backend/rag/retriever.py`
- **Deps:** T2
- **Pasos:** Cargar nodos del PKG (personas, lugares, objetos, eventos, rutinas) como documentos a ChromaDB con embeddings. `retriever.query(texto, k)` devuelve contexto relevante. Usar embeddings de Gemini (`text-embedding-004`) o `sentence-transformers` local si no hay red.
- **HECHO:** query "¿quién es Sofía?" recupera el nodo nieta.

### T4 [P0] Orquestador + RBAC router
- **Archivos:** `backend/orchestrator/router.py`, `agents.py`, `tools.py`, `guardrails.py`
- **Deps:** T3, config Gemini (ver `docs/setup/gemini-api-guide.md`)
- **Pasos:** LangGraph graph. `router.py` recibe `{rol, mensaje, patient_id}` y enruta al agente del rol (matriz RBAC spec §6). Cada agente: system prompt propio + tools permitidas + scope de datos. `guardrails.py`: el agente Médico añade disclaimer y no inventa cifras (solo lee de DB). Tools mínimas: `consultar_PKG`, `log_medicacion`, `agendar_actividad`, `reporte_clinico`, `sugerir_contacto`.
- **HECHO:** `POST /chat {rol:"paciente"...}` responde cálido usando PKG; `{rol:"medico"...}` responde técnico con disclaimer; roles distintos → datos distintos.

### T5 [P0] Motor de rutina (orquestación día-a-día)
- **Archivos:** `backend/routine/engine.py`
- **Deps:** T2, T4
- **Pasos:** Implementa la secuencia del diagrama §5. `plan_dia(patient_id)` genera eventos (check-in, medicación, actividad, monitoreo, conexión, cierre). `elegir_actividad()` evita repetir las últimas N actividades (anti-repetición). Escalado: si biomarcador/sensor supera umbral → crea Event tipo alerta para el cuidador.
- **HECHO:** `GET /routine/1/today` devuelve agenda con medicación + actividad no repetida + ≥1 punto de conexión humana.

### T6 [P1] Servicio biomarcadores (inferencia en vivo)
- **Archivos:** `backend/biomarkers/extract.py`, `predict.py`
- **Deps:** modelo.pkl del track ML
- **Pasos:** `extract(audio)` → Whisper transcribe + librosa/parselmouth (MFCC, F0, jitter, shimmer) + spaCy-es (TTR, long. oración) + webrtcvad (pausas). `predict(features, ses_metadata)` carga modelo.pkl y devuelve riesgo. Si no hay modelo aún, stub que devuelve score simulado coherente.
- **HECHO:** `POST /biomarkers/analyze` con audio devuelve features + riesgo; se guarda en DB.

### T7 [P1] SES Personalizer
- **Archivos:** `backend/ses/personalizer.py`
- **Deps:** T6
- **Pasos:** Ajusta umbral de riesgo según metadata (escolaridad, zona, IDH → estimación de reserva cognitiva). Inyecta la covariable SES al vector antes de `predict`. Documenta el ajuste para trazabilidad.
- **HECHO:** mismo audio con `escolaridad=primaria` vs `universitaria` produce interpretación de riesgo distinta y explicable.

### T8 [P2] Endpoints del Dashboard Gemelo
- **Archivos:** amplía `backend/main.py`
- **Deps:** T2, T6
- **Pasos:** `GET /twin/1/trend` (serie temporal de biomarcadores), `GET /twin/1/alerts`, `GET /twin/1/snapshot`.
- **HECHO:** frontend puede pintar tendencia + alertas.

---

## TRACK FRONTEND (dev frontend, delega Alvaro)

### F1 [P0] Scaffold React + Vite + layout multi-rol
- **Archivos:** `frontend/*`
- **Pasos:** Vite + React. Selector de rol (5 roles). Router a 5 vistas. Diseño limpio, accesible (fuente grande para paciente). Consumir `VITE_API_URL`.
- **HECHO:** cambiar rol cambia la vista.

### F2 [P0] Vista Paciente — chat de voz
- **Deps:** F1, T4
- **Pasos:** Web Speech API (STT `SpeechRecognition` es-ES + TTS `speechSynthesis`). Botón hablar → transcribe → `POST /chat` → reproduce respuesta. UI grande, cálida, foto de "Don José".
- **HECHO:** conversación por voz de ida y vuelta funciona.

### F3 [P0] Dashboard Gemelo Cognitivo
- **Deps:** F1, T8
- **Pasos:** Gráfico de tendencia (recharts) de biomarcadores + tarjetas de alerta + snapshot (estado cognitivo/emocional/adherencia). **Es el pegamento visual — que se vea impecable.**
- **HECHO:** pinta tendencia longitudinal + alertas reales de la API.

### F4 [P1] Vistas Cuidador y Médico
- **Deps:** F1, T4, T5
- **Pasos:** Cuidador: agenda del día (motor de rutina) + alertas + botón log medicación. Médico: reporte de señales clínicas del habla + tabla de tendencia + disclaimer visible.
- **HECHO:** cada vista muestra datos y tono correctos por rol.

### F5 [P2] Integración BLE con ESP32
- **Deps:** F4, hardware H1
- **Pasos:** Web Bluetooth API. Conectar al ESP32, leer FC/pasos, enviar comando de recordatorio (vibración).
- **HECHO:** navegador muestra FC en vivo y dispara vibración.

---

## TRACK ML (ver prompt dedicado `docs/plan/PROMPT-entrenamiento.md`)

### M1 [P0] Descargar dataset + EDA
### M2 [P0] Pipeline de features (audio → tabla)
### M3 [P0] Baseline `P(AD|Voz)` — XGBoost/SVM/RF
### M4 [P0] Modelo `P(AD|Voz, SES)` + comparación
### M5 [P0] Fairness estratificado por escolaridad + export modelo.pkl

---

## TRACK HARDWARE (ver `docs/hardware/hardware-guide.md`)

### H1 [P1] Firmware ESP32 (FC + pasos + SOS + vibración vía BLE)
### H2 [P2] Ruta Arduino Uno Q (visión "¿qué estoy viendo?")

---

## TRACK CONTENIDO / PITCH (contacto-paciente + diseño)

### C1 [P0] Scripts de conversación terapéutica por función cognitiva (I-CONECT/CST) → alimentan system prompts.
### C2 [P0] Datos semilla del PKG de Don José (biografía, familia, intereses) → para T2.
### C3 [P0] Guión de pitch: frase-tesis + historia de impacto + roadmap por capas.
### C4 [P1] Mockups Capa B/C (gafas, smart home) + video demo.
### C5 [P1] Evaluación de impacto / entrevistas de validación.

---

## Orden de ejecución sugerido (2 días)

**Día 1 AM:** T1, T2, F1, M1, C1, C2 · **Día 1 PM:** T3, T4, F2, M2-M3, C3, H1
**Día 2 AM:** T5, T6, F3, F4, M4-M5, C4 · **Día 2 PM:** T7, T8, F5, integración total, ensayo demo
