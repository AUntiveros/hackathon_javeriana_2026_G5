# Spec de diseño — Ecosistema de inteligencia aumentada para Alzheimer
## Prototipo hackathon (2 días) · Cuidado del adulto mayor con IA

> Fecha: 2026-07-02
> Estrategia aprobada: **Opción A** — dos tracks paralelos (biomarcadores de voz + chatbot multi-rol RBAC) unidos visualmente por el **Dashboard Gemelo Cognitivo**.
> Documentos fuente: `Hackathon_Master.md`, `Revision_Sistematica_Asistentes_IA_Alzheimer_2023-2026.md`.

---

## 1. Propósito y frase-tesis

> *"Un ecosistema de inteligencia aumentada que preserva la identidad, la autonomía y las relaciones humanas de las personas con Alzheimer, usando la IA para fortalecer —y nunca sustituir— el vínculo entre el paciente, su familia, sus cuidadores, su comunidad y su equipo de salud."*

Regla de oro: **la IA es el director de orquesta, no el solista.** No construimos un chatbot; construimos un orquestador de la red de cuidado (concepto propio: *Human-Augmented AI*).

## 2. Qué se entrega en la hackathon (alcance real)

Tres capas, con la línea dura entre "se construye" y "se pinta":

### Capa A — SE CONSTRUYE (comprometido)
1. **Chatbot multi-rol con RBAC** — 5 agentes (Paciente, Cuidador, Médico, Familiar, Comunidad), orquestados con LangGraph + Gemini 2.5 Flash. El RBAC ES el router de roles del orquestador: cada rol tiene system prompt, tono, scope de datos y herramientas propias.
2. **Pipeline de biomarcadores del habla + experimento SES** — Whisper → librosa/parselmouth/spaCy-es → clasificador. Experimento estrella: `P(AD|Voz)` vs `P(AD|Voz, Contexto socioeconómico)`, con métricas de fairness estratificadas por escolaridad. **Este es el diferenciador científico publicable.**
3. **Dashboard Gemelo Cognitivo** — pegamento visual: integra biomarcadores + eventos + tendencia longitudinal + alertas (datos semilla + resultados reales del pipeline).
4. **Conversación terapéutica** — prompts estructurados estilo I-CONECT/CST por función cognitiva.
5. **Orquestación día-a-día del paciente** — motor de rutina: agenda, medicación, actividades no repetitivas, reminiscencia, check-ins de voz, escalado de alertas al cuidador. (Ver diagrama dedicado.)
6. **Hardware wearable ESP32** — FC (MAX30102) + pasos (IMU) + botón SOS + recordatorio por vibración, vía BLE al frontend.

### Capa B — SE MOCKEA (demo visual convincente, no producción)
- Panel médico con señales clínicas derivadas del habla ("subió 25% la repetición de preguntas en 3 semanas").
- Orquestación de la red humana ("hoy sería buen día para llamar a tu nieta Sofía").
- Ubicación en tiempo real / geofence del paciente.

### Capa C — ROADMAP (solo slides + papers de respaldo)
- Smart glasses con visión ("¿qué estoy viendo?", reconocimiento facial). **Sube a demo real SOLO si prestan el Arduino Uno Q (Qualcomm, corre modelos on-device).**
- Smart home IoT, cámara ambiental Edge AI, sensores biomédicos extra, Social/Home Digital Twin completo, memoria espacial aumentada (SLAM), Federated Learning.

## 3. Arquitectura C4 y diagramas

Todos los diagramas viven en `docs/diagrams/arquitectura.md` (mermaid). Cubren:
- C4 Nivel 1 (Contexto), Nivel 2 (Contenedores), Nivel 3 (Componentes del orquestador).
- Flujo del loop cerrado conversación → biomarcadores → gemelo → personalización.
- **Orquestación del día-a-día del paciente** (secuencia detallada, requerida explícitamente).
- Diagrama de despliegue.
- Máquina de estados del wearable ESP32.

## 4. Stack técnico

| Capa | Elección | Razón |
|---|---|---|
| LLM orquestador + agentes | **Gemini 2.5 Flash** | Blueprint del paper Electronics 2026; tier gratis; function-calling nativo |
| Framework agéntico | **LangGraph + LangChain** | Estándar 2025-26, trazabilidad anti-alucinación |
| RAG | **ChromaDB** (vector) + PKG semilla JSON | GraphRAG queda roadmap; vector basta para MVP |
| Backend | **FastAPI** (Python) | Rápido, async, un solo lenguaje con el ML |
| STT biomarcadores | **Whisper** (small/medium ES) | Transcripción + timestamps de pausas |
| Features acústicas | **librosa + praat-parselmouth** | MFCC, F0, jitter, shimmer, HNR, CPP |
| Features léxicas/sintácticas | **spaCy `es_core_news_lg`** | TTR, MATTR, longitud de oración, complejidad |
| Pausas / VAD | **webrtcvad** | Silencios y disfluencias |
| Clasificador | **XGBoost / RandomForest / SVM** (sklearn) | Rápido, interpretable, baseline vs +SES |
| Modelos de habla a comparar | **wav2vec2-xls-r-es, Whisper-embeddings, HuBERT** | El "paper": performance en español + efecto metadata |
| Frontend | **React + Vite** + Web Speech API | Voice-first sin infra extra |
| STT/TTS chatbot en vivo | Web Speech API (navegador) | Cero costo para demo |
| DB | **SQLite** (dev) → Postgres (opcional) | Cero setup para hackathon |
| Hardware | **ESP32 + MAX30102 + MPU6050** | Barato, BLE nativo; Arduino Uno Q como stretch |

## 5. Modelo de datos (núcleo mínimo)

```
Patient(id, nombre, edad, sexo, ses_metadata{escolaridad, zona, idh, lengua_materna,
        ocupacion, reserva_cognitiva_est}, personalidad, rutina_base)
Event(id, patient_id, timestamp, tipo{medicacion|actividad|conversacion|alerta|cita|salida},
      payload, estado)
Biomarker(id, patient_id, timestamp, categoria, features{...}, riesgo_score, modelo_version)
TwinSnapshot(id, patient_id, timestamp, estado_cognitivo, estado_emocional, riesgo,
             autonomia, adherencia, carga_cuidador)
PKGNode(id, patient_id, tipo{persona|lugar|objeto|evento|rutina}, atributos, embeddings)
PKGEdge(src, dst, relacion)
Role(nombre, scope_datos[], herramientas[], system_prompt)
```

## 6. RBAC — matriz de roles

| Rol | Objetivo | Tono | Scope de datos | Herramientas | NO hace |
|---|---|---|---|---|---|
| Paciente | Acompañar, estimular cognición, extraer biomarcadores, preservar identidad | Cálido, culturalmente pertinente | Su PKG, su rutina | reminiscencia, recordatorio, check-in de voz | diagnosticar, alarmar |
| Cuidador | Cuidador aumentado: qué preguntar/evitar, alertas, control de tareas | Práctico, empático | Rutina, adherencia, alertas, tendencia | agenda, log medicación, plan de actividades | reemplazar juicio del cuidador |
| Médico | Resumir señales clínicas del habla + sensado, trazabilidad | Técnico, conciso, con fuentes | Biomarcadores, tendencias, adherencia | reporte clínico, ver histórico | sustituir decisión clínica |
| Familiar | Sugerir contacto, preparar contexto, reminiscencia | Cercano, motivador | Estado general, temas de conversación | sugerir llamada, temas | invadir privacidad del paciente |
| Comunidad | Conectar pares con intereses comunes | Social, inclusivo | Intereses, disponibilidad | matching de pares | exponer datos sensibles |

## 7. Seguridad y ética

- La IA **no diagnostica**: alerta y acompaña; la decisión es del médico.
- Todos los agentes anclados en RAG con trazabilidad → mitiga alucinación; ninguno da consejo médico no verificado.
- Disclaimers de formato obligatorios en respuestas del agente Médico.
- Datos sensibles nunca a la nube en el mock (edge-first en el discurso).
- Consentimiento informado; alineación con Ley N° 29733 (Perú), ODS 3, Plan Nacional de Alzheimer 2026-2028.

## 8. Riesgos y mitigación

| Riesgo | Mitigación |
|---|---|
| Dataset Ivanova tarde (2-5 días) | **MultiConAD (HuggingFace) desde día 1**; Ivanova es upgrade opcional |
| Alvaro cuello de botella (2 backends) | Delegar TODO frontend y contenido; Alvaro solo backends + integración |
| Hardware falla en vivo | **Grabar video del ESP32 funcionando** como backup; ESP32 seguro, Uno Q bonus |
| Sobre-alcance | Línea dura Capa A vs C en el pitch |
| LLM alucina consejo médico | RAG + reglas de formato + disclaimers |

## 9. Criterios de "hecho" para la demo

- [ ] Paciente conversa por voz; el agente recuerda datos del PKG ("Don José").
- [ ] Conversación dispara extracción de ≥1 biomarcador visible en el dashboard.
- [ ] Cambiar de rol cambia vista, tono y datos accesibles (RBAC demostrable en vivo).
- [ ] Experimento entrenado: tabla AUC baseline vs +SES, con fairness por escolaridad.
- [ ] Dashboard Gemelo muestra tendencia longitudinal + ≥1 alerta.
- [ ] ESP32 envía FC/pasos por BLE y recibe recordatorio (o video backup).
- [ ] Orquestación día-a-día: agenda del paciente con medicación + actividad no repetitiva.
- [ ] Pitch con frase-tesis, historia de impacto (quechuahablante mal clasificado), roadmap por capas.
