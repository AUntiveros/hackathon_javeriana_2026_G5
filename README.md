# Ecosistema de inteligencia aumentada para Alzheimer 🎼

Prototipo de hackathon (2 días) · Cuidado del adulto mayor con IA.
**La IA es el director de orquesta de la red de cuidado, no el solista.**

## Documentación

| Doc | Qué contiene |
|---|---|
| [Spec de diseño](docs/specs/2026-07-02-ecosistema-alzheimer-design.md) | Arquitectura, C4, stack, capas A/B/C, RBAC, criterios de HECHO |
| [Diagramas (mermaid)](docs/diagrams/arquitectura.md) | C4, loop biomarcadores, **orquestación día-a-día**, ESP32, despliegue |
| [Plan de implementación](docs/plan/implementation-plan.md) | Tareas atómicas troceadas por track (para ejecutar con modelo ligero) |
| [PROMPT de entrenamiento](docs/plan/PROMPT-entrenamiento.md) | Pegar en terminal paralela → entrena el modelo de predicción (impacto novedoso) |
| [Guía Gemini](docs/setup/gemini-api-guide.md) | Cómo obtener y configurar la API key |
| [Guía de hardware](docs/hardware/hardware-guide.md) | BOM ESP32, pinout, firmware, ruta Arduino Uno Q |

## Arranque rápido — RAG (prototipar YA)

```bash
cd "D:/UNIDAD D/UNIVERSIDAD/2026-1/Hackathon Javeriana"
python -m venv .venv && .venv/Scripts/activate         # Windows
pip install -r backend/requirements.txt
python -m spacy download es_core_news_lg               # para biomarcadores luego
cp backend/.env.example backend/.env                   # y pega tu GEMINI_API_KEY

python -m backend.rag.ingest                           # carga el PKG de Don José
python -m backend.rag.retriever "¿quién es Sofía?"     # prueba de recuperación
python -m backend.rag.demo_chat "No sé quién me llamó ayer."   # RAG + Gemini end-to-end
```

Sin GEMINI_API_KEY, el RAG funciona igual con embeddings offline (sentence-transformers);
solo `demo_chat` necesita la key de Gemini.

## Tracks (5 personas)

- **Alvaro** — backend orquestador + RBAC + biomarcadores + integración + hardware.
- **Frontend** — React/Vite, vistas por rol, dashboard Gemelo, BLE.
- **Contacto-paciente** — scripts terapéuticos, PKG semilla, entrevistas, pitch.
- **Diseño** — identidad, mockups Capa B/C, video, slides.
- **Flexible** — data (MultiConAD), baseline, QA, docs.

## Backend — cómo correr

```bash
pip install fastapi uvicorn sqlmodel chromadb
python -m backend.db.seed          # puebla Don José + 30 días de biomarcadores
python -m backend.rag.ingest       # carga el PKG (necesita GEMINI_API_KEY o sentence-transformers)
uvicorn backend.main:app --reload  # API en http://localhost:8000/docs
```

Endpoints: `/health`, `POST /chat {rol,mensaje}`, `/patients/{id}`, `/routine/{id}/today`,
`/twin/{id}/trend`, `/twin/{id}/snapshot`, `/ses/{id}/riesgo`. Sin GEMINI_API_KEY el chat corre
en modo offline (muestra scope/contexto); con key responde con Gemini.

## Estado
- [x] Investigación estado del arte
- [x] Arquitectura + C4 + diagramas
- [x] Plan troceado + prompts de ejecución
- [x] Scaffold RAG (PKG + ingest + retriever + demo)
- [x] Backend orquestador: DB+seed (T1-T2), RBAC 5 roles (T4), motor rutina (T5), SES (T7), endpoints dashboard (T8) — probado
- [ ] Biomarcadores en vivo (T6) — espera `ml/model.pkl` de la terminal paralela
- [ ] Frontend (F1–F5)
- [ ] Modelo entrenado (M1–M5) — corriendo en terminal paralela
- [x] Firmware ESP32 (H1): .ino (FC+pasos+caída+SOS+vibración BLE) + página Web Bluetooth de prueba — pendiente flashear en hardware real
- [x] Uno Q (H2): asistente de entorno completo — objetos "¿qué es esto?", "mis objetos", memoria espacial, reconocimiento facial, voz (altavoz paralelo edge/cloud), sync a la DB del asistente — flujo probado (stub); pendiente modelo/cámara/mic físicos en el Uno Q
- [ ] Frontend (F1–F5) — en terminal paralela
