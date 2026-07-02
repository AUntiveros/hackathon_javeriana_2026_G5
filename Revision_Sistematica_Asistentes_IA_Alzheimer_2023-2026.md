# Revisión sistemática del estado del arte (2023–2026)
## Asistentes inteligentes para personas con Alzheimer y otras demencias: autonomía, calidad de vida y apoyo al cuidado

> **Documento de trabajo para hackathon — Cuidado del adulto mayor con tecnologías emergentes**
> Enfoque: preservación de autonomía, calidad de vida y redes de cuidado (NO diagnóstico ni tratamiento farmacológico).
> Alcance temporal prioritario: enero 2025 – junio 2026, con base 2023–2024.

---

## 0. Cómo usar este documento

Este documento es un **mapa de investigación vivo**, no un paper cerrado. Está organizado en tres capas:

1. **Ejes tecnológicos** (secciones 1–7): qué existe, qué funciona, qué papers lo respaldan.
2. **Catálogo de papers** (sección 8): fichas detalladas de los trabajos más relevantes.
3. **Análisis y oportunidades** (secciones 9–11): tendencias, gaps, y líneas concretas de innovación para la hackathon.

**Nota metodológica sobre honestidad de datos:** los números de participantes, métricas y años provienen de las fuentes citadas. Donde un dato no pudo verificarse con certeza se marca con ⚠️. Los TRL (Technology Readiness Level) son *estimaciones propias* basadas en el grado de validación reportado, no cifras oficiales.

---

## 1. Arquitecturas de IA

### 1.1 Panorama general

El campo transitó, entre 2023 y 2026, de clasificadores estáticos y chatbots con guiones fijos hacia **sistemas agénticos** capaces de razonar sobre la trayectoria del paciente, orquestar herramientas y adaptar su comportamiento. La transición clave es de *"IA que clasifica"* a *"IA que acompaña y coordina"*.

### 1.2 Large Language Models (LLMs) como núcleo conversacional

Los LLMs son hoy el núcleo dominante de los asistentes para demencia porque soportan diálogo abierto, permiten al cuidador articular estados emocionales complejos en lenguaje natural y ofrecen interacción bajo demanda sin requerir inputs estructurados.

**Fortalezas documentadas:**
- Soporte personalizado, enriquecimiento cognitivo y predicción de cambios emocionales a partir de patrones lingüísticos.
- Generación de sesiones informativas a medida para cuidadores informales.

**Limitaciones críticas (recurrentes en toda la literatura 2025–2026):**
- **Alucinaciones**: riesgo de generar consejo médico no verificado. Es el principal obstáculo para adopción clínica.
- **Empatía simulada sin comprensión real**: los LLMs simulan empatía pero no detectan bien el distrés psicológico.
- **Falta de memoria persistente**: pierden contexto entre sesiones, dando respuestas genéricas y repetitivas — justo lo contrario de lo que necesita el cuidado longitudinal.
- **Personas cognitivamente estables como supuesto**: la mayoría de sistemas de simulación asumen pacientes cognitivamente estables, subrepresentando fenómenos propios de la demencia (repetición, recuerdo contradictorio, desorientación temporal).

### 1.3 Agentes autónomos y Multi-Agent Systems (MAS)

La arquitectura **orquestador + agentes especializados** es el patrón emergente dominante. Un agente central enruta dinámicamente las consultas del usuario a herramientas especializadas (Q&A con RAG, interpretación de documentos, agendamiento).

- **Patrón de referencia (2026):** asistente virtual médico con orquestador construido en LangChain + LangGraph, con Gemini 2.5 Flash definiendo uso de herramientas y reglas estrictas de formato para mitigar alucinaciones.
- **Integración RL + LLM (2025):** frameworks que combinan un LLM con aprendizaje por refuerzo para simular comportamientos desafiantes de personas con demencia (PLWD) durante actividades de la vida diaria (ADL), y adaptar la interacción del robot cuidador al estado cognitivo y emocional.
- **Tendencia MAS médica (2025):** frameworks modulares multi-agente con roles especializados (p.ej. MAM para diagnóstico multimodal, sistemas de "debate por capas" para diagnóstico diferencial).

### 1.4 Edge AI, On-device AI y TinyML

El monitoreo del adulto mayor empuja fuertemente hacia el **procesamiento local** por tres razones convergentes: privacidad, latencia y conectividad (crítico para zonas sin internet estable — muy relevante para LatAm).

- **Beneficios documentados del edge:** mayor vida de batería, privacidad mejorada, menor latencia, menor costo operativo. Un sistema edge de ECG con Q-CNN redujo el tiempo de respuesta 85% frente al análisis en la nube.
- **TinyML en microcontroladores:** detección de caídas en ancianos con algoritmos TinyML optimizados para MCU; localización indoor con transformers/Mamba cuantizados y destilados para correr en MCU de bajo consumo.
- **Benchmarks maduros:** MLPerf Tiny v1.3 (2025) permite comparar latencia, throughput y energía en dispositivos que corren inferencia durante días con una pila de botón.
- **Federated Learning (FL):** paradigma emergente para entrenar modelos globales sin centralizar datos crudos — clave para privacidad en salud. Se combina con edge en frameworks "dignity-aware" (Jetson Orin Nano + FL para ADL).

### 1.5 AI companions

Los compañeros de IA (software y encarnados en robots) buscan reducir soledad y aislamiento — factores de riesgo directos de deterioro cognitivo. Ver sección 5 (interacción) y 8 (catálogo) para evidencia de ensayos.

---

## 2. Sistemas de memoria

La **memoria persistente** es, según la literatura 2025–2026, el cuello de botella central para que un asistente sea útil en cuidado longitudinal de demencia. Un asistente sin memoria de largo plazo "pierde contexto entre sesiones y entrega respuestas genéricas y repetitivas".

### 2.1 Taxonomía de memoria en agentes (estado del arte)

| Tipo de memoria | Qué almacena | Sistemas de referencia (2025–2026) |
|---|---|---|
| **Long-term / short-term unificada** | Operaciones de memoria como acciones tipo herramienta | AgeMem (2026) — expone la memoria como acciones entrenadas vía RL progresivo |
| **Episódica + semántica separadas** | Eventos vividos vs conocimiento general | Nemori (2025) — separa stores episódico y semántico |
| **Asociativa tipo Zettelkasten** | Notas de memoria con enlace dinámico | A-Mem (2025) — recupera por similitud de embeddings |
| **Incremental con actualización LLM** | Extracción incremental con operaciones de update | Mem0 (2025) — variante grafo con diseño entity-centric |
| **Grafo-asociativa** | Grafos con propagación de relevancia | HippoRAG (2024), GAAMA (2026), SAGE (2026) |
| **Consolidación de memoria** | Fusión y decaimiento temporal | Área activa, sin estándar consolidado ⚠️ |

### 2.2 Continual / lifelong learning y personal knowledge bases

- El reto no resuelto es la **consolidación de memoria** (qué recordar, qué olvidar, cómo fusionar) sin catástrofe de olvido.
- Las **bases de conocimiento personales** (personal knowledge bases) son el sustrato para personalización real: preferencias, rutinas y conversaciones previas del paciente.
- **Gap crítico para demencia:** ningún sistema de memoria de agentes está diseñado específicamente para pacientes cuya *propia* memoria se degrada — el asistente debe ser el "andamio" de memoria externa, un rol conceptualmente distinto al de un asistente para usuario sano.

---

## 3. Retrieval-Augmented Generation (RAG)

### 3.1 Por qué RAG importa en este dominio

RAG ancla las respuestas del LLM en evidencia externa antes de generar, reduciendo alucinaciones y permitiendo **trazabilidad** (citar la guía clínica de origen) — requisito de confianza para uso con cuidadores y clínicos.

### 3.2 Variantes y cuál conviene

| Variante | Idea central | Relevancia para asistente de demencia |
|---|---|---|
| **RAG plano (vector)** | Recupera chunks por similitud de embeddings. Stateless, orientado a documentos. | Punto de partida. Pierde relaciones estructurales entre entidades/eventos. |
| **GraphRAG** | Recupera sobre grafo de entidades y relaciones; razonamiento multi-hop. | Mejora precisión hasta **35%** sobre vector-only en razonamiento complejo. Ideal para modelar la red de cuidado y la historia del paciente. |
| **HybridRAG** | Combina vector + grafo. | Cubre tanto recuperación factual rápida como razonamiento relacional. |
| **Agentic RAG** | Agentes deciden *si* recuperar, *de dónde* y refinan iterativamente. | Paradigma 2025–2026 para salud: interpreta intención, descompone tareas, reescribe consultas ambiguas. |
| **Temporal RAG** | Incorpora dimensión temporal en la recuperación. | Clave para trayectorias longitudinales (¿cómo estaba el paciente hace 3 meses?). |
| **Personalized / Memory-aware RAG** | Recuperación condicionada al perfil y memoria del usuario. | Núcleo de la personalización paciente-específica. Surveys 2025 ("From RAG to Agent"). |

### 3.3 Hallazgo práctico

GraphRAG **supera consistentemente** a vanilla RAG en razonamiento complejo y summarización contextual, pero la ventaja se estrecha para recuperación factual simple, donde el vector search basta (GraphRAG-Bench 2025). **La elección de operadores de grafo** (cómo se traversa y rankea) importa más que la estructura del grafo en sí — métodos como Personalized PageRank (HippoRAG) dominan.

### 3.4 Ejemplo aplicado a demencia

**ADQueryAid** (npj Biomedical Innovations, 2024): usa un **grafo de conocimiento estructurado de ADRD + LLM** para identificar la intención del cuidador. El input se enriquece contra el grafo, y un motor de razonamiento colabora con el motor de prompts para refinar la consulta y generar un prompt más dirigido al LLM. Es el ejemplo más claro de HybridRAG aplicado a soporte de cuidadores de Alzheimer.

---

## 4. Modelado del paciente

### 4.1 Digital Twins y Cognitive Digital Twins

El **gemelo digital cognitivo** crea modelos virtuales dinámicos y personalizados del sistema cognitivo individual, para monitoreo continuo, modelado predictivo e intervenciones de precisión.

**Estado del arte (revisión sistemática PRISMA, 78 estudios, 2017–2025):**
- Progresión clara de marcos conceptuales a aplicaciones clínicas validadas, con **aceleración notable desde 2023** (42 estudios = 54% del total).
- Integra ML, DL y LLMs para sintetizar biomarcadores digitales diversos en perfiles cognitivos adaptativos.

**Aplicaciones documentadas (2025–2026):**
- **Gemelos digitales para ensayos clínicos de AD:** modelos CRBM entrenados en 6,736 sujetos generan "gemelos" que predicen el outcome placebo de cada participante, reduciendo el tamaño muestral necesario ~9–15% (Alzheimer's & Dementia TRCI, 2025).
- **Roadmap de aging digital twins (Ageing Research Reviews, ene 2026):** monitoreo en tiempo real y analítica predictiva para geriatría de precisión.
- **Language-Based Digital Twins (arXiv, 2026):** gemelos basados en lenguaje para asistencia cognitiva de adultos mayores, usando el habla como biomarcador escalable y no invasivo.

⚠️ **Nota de honestidad:** la mayor parte del trabajo en gemelos digitales de Alzheimer está orientado a *ensayos clínicos y predicción de progresión*, NO a asistencia diaria. Aquí hay un gap de aplicación aprovechable.

### 4.2 Personal Knowledge Graphs, Life Logs y modelado de rutina

- **Personal Knowledge Graphs (PKG):** representan al paciente como grafo de entidades (personas, lugares, rutinas, objetos) y relaciones. Sustrato natural para GraphRAG personalizado.
- **Daily Routine Modeling + Activity Recognition:** modelar la rutina permite detectar anomalías conductuales (ver sección 6).
- **Behavioral Modeling:** modelos derivados de sensores para detectar firmas de demencia temprana (línea Poyiadzi et al. y sucesores).

---

## 5. Interacción humano-IA

### 5.1 Interfaces voice-first y conversational AI

Las interfaces **voice-first** son especialmente apropiadas para adultos mayores con deterioro cognitivo: reducen la carga de la interfaz gráfica, no requieren alfabetización digital y permiten instrucción por voz. Los asistentes de voz (smart speakers) muestran potencial para apoyar el "aging in place".

### 5.2 Social robots — evidencia de ensayos (la más sólida del documento)

Los robots sociales/asistivos (SAR) tienen la **base de evidencia clínica más robusta** de todo el campo, con múltiples RCTs y meta-análisis:

- **PARO (robot foca):** RCT grupal en adultos mayores con demencia leve mostró mejoras en función cognitiva, sistema nervioso autónomo y bienestar mental (JAMDA, 2024).
- **Robot PIO:** RCT en centros de día (Corea, n=66) mostró mejora significativa de función cognitiva (MMSE +3.9 vs +0.1 control, p<.001); efecto en depresión no significativo (PLOS ONE, 2025).
- **Meta-análisis SAR (JAMDA, 2024):** 8 RCTs, muestras de 33 a 415, mayoría >80 años. Efectos en depresión y soledad en cuidado de largo plazo.
- **RCT robot social digital (JMIR Aging, oct 2025, Japón, n=73):** reducción de soledad en adultos mayores que viven solos en comunidad — importante porque la mayoría de estudios previos eran en instituciones occidentales.

**Tendencia 2025:** integración de LLMs en robots sociales para hacerlos más adaptables y personalizados, con la salvedad recurrente del riesgo de alucinación en consejo médico.

### 5.3 Ambient Intelligence y Human-centered AI

- **Ambient Intelligence:** sensores ambientales (movimiento, puertas, presión) que monitorean el entorno completo, no solo métricas individuales.
- **Human-centered AI:** énfasis creciente en diseño centrado en dignidad ("dignity-aware AI"), consentimiento y aceptación por parte de adultos mayores y cuidadores (estudios de actitudes vía NLP + análisis temático, 2025).

---

## 6. Monitoreo pasivo

### 6.1 Smartphone sensing — el eje con más tracción reciente

El **sensado pasivo por smartphone** es la vía más escalable y de menor fricción: aprovecha interacciones cotidianas del dispositivo para monitorear funciones en entornos reales durante periodos largos, sin carga de evaluación.

**Evidencia clave 2025–2026:**
- **Deep learning + routine-aware augmentation + personalización demográfica (arXiv, sep 2025):** ventana deslizante de 30 días sobre features conductuales diarias; estudio prospectivo de 1 año en adultos ≥65, con "día válido" = ≥14h de cobertura de sensado.
- **TechSANS study (Alzheimer's & Dementia, ene 2026):** biomarcadores de marcha y tipeo desde sensado pasivo de smartphone (n=21, ≥65 años, 1 año). Captura tipo de movimiento, marcha, ubicación, uso del teléfono, tipeo y comunicación.
- **ALLFTD Mobile App (Alzheimer's & Dementia, ene 2025):** en demencia frontotemporal (n=199), features pasivas de smartphone solas (AUC=0.75) superaron al MoCA (AUC=0.66) para distinguir FTD prodrómica; combinadas AUC=0.80.

### 6.2 Sensores, GPS, IMU y multimodalidad

- **GPS:** la varianza de ubicación correlaciona con síntomas (línea de mobility features).
- **IMU:** detección de caídas y reconocimiento de actividad (SISFall y sucesores, con FL + edge).
- **Wearables consumer-grade (npj Digital Medicine, ene 2026):** predicción pasiva de 21 outcomes cognitivos y de salud mental en 82 adultos sanos; smartwatch + smartphone para detección remota de MCI (Nature Medicine, 2025).
- **Sueño y actividad diurna (Sensors, oct 2025):** Garmin Vivoactive5 + Somnofy en residentes con demencia — relación actividad diurna/calidad de sueño.

### 6.3 Voice biomarkers y detección de anomalías conductuales

- **Voice biomarkers:** ver el proyecto NeuroTrace (documento separado). Fluidez, pausas, jitter, TTR como marcadores; los de *timing* transfieren mejor entre idiomas.
- **Behavioral anomaly detection:** frameworks edge-IoT con sensores no-wearable detectan desviaciones de patrones normales (p.ej. inmovilidad prolongada, wandering vía sensores de puerta) — Sensors 2025, MDPI.
- **Context awareness:** integración de rutina + entorno para reducir falsos positivos.

---

## 7. Redes de apoyo

### 7.1 El cuidador como usuario central

El cuidado informal representa **~50% de las tareas de cuidado a nivel global**. La literatura 2025–2026 enfatiza que la tecnología debe ser **apoyo al clínico y al cuidador, no reemplazo**.

**Sistemas de soporte a cuidadores (2024–2026):**
- **Conversational AI para cuidadores de Alzheimer (npj Biomedical Innovations, 2024):** ADQueryAid — grafo ADRD + LLM para guía personalizada.
- **LLMs para cuidadores de demencia temprana (JMIR / mixed methods, 2025):** evaluación con 32 preguntas en 4 dominios (valores culturales, apoyo social, estilo de afrontamiento, alfabetización en demencia); reclutamiento de 12 participantes (ene 2025).
- **Mapping Caregiver Needs to AI Chatbot Design (arXiv, 2026):** identifica fortalezas y gaps de los chatbots en salud mental de cuidadores ADRD.
- **REACH + robótica social (Frontiers Robotics & AI, dic 2025):** adapta la intervención REACH II (coaching personalizado basado en evidencia) a robots sociales para cuidadores informales.
- **Care to Plan (CtP):** herramienta web de recomendaciones de soporte a medida para cuidadores.

### 7.2 Coordinación de cuidado y decisión compartida

- **Care coordination + shared decision making:** áreas menos maduras tecnológicamente ⚠️.
- **Dynamic agent affiliation (DIS '24):** pregunta abierta clave — *¿para quién trabaja el agente de IA en la red de cuidado del adulto mayor?* (paciente vs cuidador vs clínico). Problema de gobernanza no resuelto.
- **Family-centered / community care:** el modelo de "navegador digital" y el compartir social digital entre cuidadores (combate aislamiento) son líneas con evidencia inicial.

---

## 8. Catálogo de papers (fichas detalladas)

> Fichas priorizadas por relevancia y recencia. Los campos sin dato confiable se marcan ⚠️.

### 8.1 — ADQueryAid: Conversational AI para cuidadores de Alzheimer
- **Referencia:** Empowering Alzheimer's caregivers with conversational AI. *npj Biomedical Innovations*, 2024.
- **DOI:** 10.1038/s44385-024-00004-8 · **Año:** 2024 · **País:** EE.UU. ⚠️
- **Objetivo:** guía personalizada a cuidadores identificando intención de la consulta.
- **Arquitectura:** grafo de conocimiento ADRD + LLM (HybridRAG). Motor de razonamiento + motor de prompts.
- **Tecnologías:** knowledge graph, LLM, contextualización de consulta.
- **Memoria:** semántica (grafo estructurado). **Grafos:** ✅ central. **RAG:** ✅ (graph-augmented). **IA generativa:** ✅.
- **Validación clínica:** preliminar. **Participantes:** ⚠️.
- **Resultados:** identificación precisa de intención del cuidador; guía más dirigida.
- **Limitaciones:** riesgo de alucinación; validación limitada.
- **TRL estimado:** 4–5. **Oportunidad:** extender a español + red de cuidado multi-agente.

### 8.2 — Digital Twin Cognition (revisión sistemática)
- **Referencia:** Digital Twin Cognition: AI-Biomarker Integration in Biomimetic Neuropsychology. *Biomimetics (MDPI)*, 2025;10(10):640.
- **DOI:** 10.3390/biomimetics10100640 · **Año:** 2025 · **PMCID:** PMC12561581
- **Objetivo:** sintetizar la integración de biomarcadores IA en marcos de gemelo digital cognitivo.
- **Metodología:** revisión sistemática PRISMA 2020, 78 estudios (2017–2025).
- **Tecnologías:** ML, DL, LLMs, biomarcadores multimodales.
- **Memoria:** N/A (revisión). **Grafos:** parcial. **RAG:** N/A. **Generativa:** discutida.
- **Resultado clave:** aceleración de publicaciones desde 2023 (54%); progresión de conceptual a validado.
- **TRL estimado:** campo 3–6 (heterogéneo). **Oportunidad:** gemelo digital para asistencia diaria (no solo ensayos).

### 8.3 — Passive smartphone sensing con routine-aware augmentation
- **Referencia:** Deep Learning-Based Detection of Cognitive Impairment from Passive Smartphone Sensing. *arXiv*:2509.23158, 2025.
- **Año:** 2025 · **País:** EE.UU. ⚠️
- **Objetivo:** detectar deterioro cognitivo desde sensado pasivo con aumento consciente de rutina y personalización demográfica.
- **Metodología:** ventana deslizante 30 días; features conductuales diarias; estudio prospectivo 1 año, ≥65 años.
- **Tecnologías:** deep learning, smartphone sensing, personalización demográfica.
- **Memoria:** temporal (secuencias). **Grafos:** ✗. **RAG:** ✗. **Generativa:** ✗.
- **Validación:** UDS v3 del NACC, evaluado por neuropsicólogo. **Participantes:** cohorte en curso (may 2023–dic 2024).
- **Limitaciones:** requiere ≥23 días válidos; imputación de faltantes.
- **TRL estimado:** 4. **Oportunidad:** la *personalización demográfica* es exactamente tu idea de metadata SES.

### 8.4 — TechSANS: gait y typing biomarkers pasivos
- **Referencia:** Passive Smartphone Sensing Reveals Gait and Typing Biomarkers of Cognitive Impairment. *Alzheimer's & Dementia*, 2026.
- **DOI:** 10.1002/alz70856_107368 · **Año:** 2026 · **País:** EE.UU. (UT Austin)
- **Objetivo:** descubrir biomarcadores digitales pasivos para evaluación funcional escalable.
- **Metodología:** n=21 (≥65), 1 año, app iOS; motion, marcha, ubicación, uso, tipeo, comunicación.
- **Memoria:** temporal. **Grafos:** ✗. **RAG:** ✗. **Generativa:** ✗.
- **Resultados:** modelos lineales mixtos generalizados controlados por edad separan grupos.
- **Limitaciones:** muestra pequeña (17 normales, 4 MCI/demencia).
- **TRL estimado:** 4. **Oportunidad:** replicable de bajo costo en LatAm.

### 8.5 — ALLFTD Mobile App: smartphone > MoCA
- **Referencia:** Passively collected data from smartphones improves detection of FTD compared to the MoCA. *Alzheimer's & Dementia*, 2025.
- **DOI:** 10.1002/alz.090571 · **Año:** 2025 · **PMCID:** PMC11710252
- **Objetivo:** detectar FTD prodrómica/sintomática vs MoCA con datos pasivos.
- **Metodología:** n=199, hasta 6 meses de monitoreo pasivo; batería y pasos como proxies.
- **Resultados:** features pasivas AUC=0.75 > MoCA AUC=0.66 (p<0.01); combinadas AUC=0.80.
- **TRL estimado:** 4–5. **Oportunidad:** demuestra que lo pasivo puede superar al test estándar.

### 8.6 — Robot PIO (RCT)
- **Referencia:** Social robot PIO intervention for cognitive function and depression in older adults with mild-moderate dementia. *PLOS ONE*, 2025.
- **DOI:** 10.1371/journal.pone.0321745 · **Año:** 2025 · **País:** Corea del Sur
- **Metodología:** RCT, 2 centros de día, n=66 (33 exp / 33 control), 12 sesiones/6 semanas.
- **Resultados:** MMSE +3.9±3.66 (exp) vs +0.1±4.13 (control), p<.001; depresión no significativa.
- **Memoria:** ⚠️. **Generativa:** ⚠️. **Validación clínica:** ✅ RCT.
- **TRL estimado:** 6–7. **Oportunidad:** protocolo de intervención adaptable a bajo costo.

### 8.7 — RCT robot social digital (Japón, comunidad)
- **Referencia:** Evaluating Digital Social Robots in Reducing Loneliness Among Community-Dwelling Older Adults in Japan. *JMIR Aging*, 2025;8:e74422.
- **DOI:** 10.2196/74422 · **Año:** 2025 · **País:** Japón
- **Metodología:** RCT + análisis cualitativo, n=73, ≥65 viviendo solos.
- **Resultados:** reducción de soledad; outcomes secundarios de bienestar, risa, competencia en salud.
- **TRL estimado:** 6. **Oportunidad:** foco en comunidad (no institución), replicable.

### 8.8 — Integración RL + AI Agents para robótica en demencia
- **Referencia:** Integrating Reinforcement Learning and AI Agents for Adaptive Robotic Interaction in Dementia Care. *arXiv*:2501.17206, 2025.
- **Año:** 2025.
- **Arquitectura:** LLM (GPT-4o) + framework RL; agente "Robot Caregiver" adapta interacción a estado cognitivo/emocional durante ADLs.
- **Memoria:** de estado (RL). **Grafos:** ✗. **RAG:** ✗. **Generativa:** ✅.
- **Limitaciones:** simulación, no despliegue clínico. Independiente del LLM específico.
- **TRL estimado:** 3–4. **Oportunidad:** simular comportamientos PLWD para entrenar cuidadores.

### 8.9 — Asistente virtual multi-agente (LLM + RAG) para clínica
- **Referencia:** Designing an Architecture of a Multi-Agentic AI-Powered Virtual Assistant Using LLMs and RAG for a Medical Clinic. *Electronics (MDPI)*, 2026;15(2):334.
- **DOI:** 10.3390/electronics15020334 · **Año:** 2026
- **Arquitectura:** orquestador + agentes especializados (Q&A RAG, interpretación de documentos, agendamiento). LangChain + LangGraph + Gemini 2.5 Flash.
- **Memoria:** de sesión. **Grafos:** parcial. **RAG:** ✅. **Generativa:** ✅.
- **Resultado:** trazabilidad de pasos de razonamiento; mitigación de alucinaciones vía reglas de formato.
- **TRL estimado:** 5. **Oportunidad:** blueprint arquitectónico casi directo para tu asistente.

### 8.10 — GAAMA: Graph Augmented Associative Memory for Agents
- **Referencia:** GAAMA: Graph Augmented Associative Memory for Agents. *arXiv*:2603.27910, 2026.
- **Año:** 2026.
- **Objetivo:** memoria de largo plazo con recuperación grafo-estructurada y propagación asociativa.
- **Memoria:** long-term asociativa (grafo). **Grafos:** ✅. **RAG:** ✅ (GraphRAG). **Generativa:** ✅.
- **Contexto:** compite con A-Mem, Mem0, Nemori, AgeMem, HippoRAG.
- **TRL estimado:** 3. **Oportunidad:** sustrato de memoria para asistente que sea "andamio" de memoria del paciente.

### 8.11 — Redefining Elderly Care with Agentic AI
- **Referencia:** Redefining Elderly Care with Agentic AI: Challenges and Opportunities. *arXiv*:2507.14912, 2025.
- **Año:** 2025.
- **Tipo:** revisión/posicionamiento. Cubre asistentes LLM, monitoreo en tiempo real, analítica predictiva, soporte a decisión clínica.
- **TRL estimado:** N/A. **Oportunidad:** marco conceptual para justificar la propuesta.

### 8.12 — Human-Centered Ambient and Wearable Sensing (scoping review)
- **Referencia:** Human-Centered Ambient and Wearable Sensing for Automated Monitoring in Dementia Care: A Scoping Review. *arXiv*:2603.05516, 2026.
- **Año:** 2026.
- **Tipo:** scoping review. Cubre radar mmWave, marcha, detección de anomalías, aging-in-place.
- **Gap señalado:** "dynamic agent affiliation" — para quién trabaja el agente en la red de cuidado.
- **TRL estimado:** campo variable. **Oportunidad:** mapa completo de modalidades de sensado.

### 8.13 — Edge AI + anomaly detection con sensores no-wearable
- **Referencia:** An Innovative IoT and Edge Intelligence Framework for Monitoring Elderly People Using Anomaly Detection. *Sensors (MDPI)*, 2025;25(6):1735.
- **DOI:** 10.3390/s25061735 · **Año:** 2025 · **País:** Italia
- **Arquitectura:** framework edge-IoT, sensores ambientales (movimiento, puertas), detección de anomalías en tiempo real.
- **Memoria:** temporal (patrones). **Grafos:** ✗. **RAG:** ✗. **Generativa:** ✗.
- **Uso demencia:** detección de wandering e inmovilidad prolongada.
- **TRL estimado:** 5. **Oportunidad:** privacidad por diseño (no cámara, no cloud).

### 8.14 — Language-Based Digital Twins for Elderly Cognitive Assistance
- **Referencia:** Language-Based Digital Twins for Elderly Cognitive Assistance. *arXiv*:2606.27334, 2026.
- **Año:** 2026.
- **Objetivo:** gemelo digital basado en lenguaje usando el habla como biomarcador escalable.
- **Memoria:** episódica/temporal (conversacional). **Grafos:** ⚠️. **Generativa:** ✅.
- **Nota:** critica que la mayoría de enfoques se centran en *predicción* más que en *asistencia*.
- **TRL estimado:** 3. **Oportunidad:** puente directo entre NeuroTrace (habla) y asistente diario.

### 8.15 — DemMA: Dementia Multi-Turn Dialogue Agent
- **Referencia:** DemMA: Dementia Multi-Turn Dialogue Agent with Expert-Guided Reasoning and Action Simulation. *arXiv*:2601.06373, 2026.
- **Año:** 2026.
- **Objetivo:** modelar la demencia como estado cognitivo en progresión, generando patrones de quiebre conversacional que evolucionan por turno.
- **Aporte:** a diferencia de PATIENT-Ψ/PatientSim (asumen pacientes estables), captura repetición, recuerdo contradictorio y desorientación temporal.
- **TRL estimado:** 3. **Oportunidad:** simulador para entrenar/evaluar el asistente.

---

## 9. Análisis comparativo: tendencias tecnológicas

### 9.1 Tendencias predominantes (2025–2026)

1. **De chatbot a agente orquestador.** El patrón dominante es orquestador central + agentes/herramientas especializadas (LangGraph, MAS).
2. **RAG anclado en grafos.** GraphRAG/HybridRAG se imponen para razonamiento relacional y trazabilidad; +35% sobre vector-only en tareas complejas.
3. **Memoria como ciudadano de primera clase.** Explosión de sistemas de memoria de agentes (Mem0, A-Mem, Nemori, GAAMA, AgeMem) — pero ninguno diseñado para memoria *degradada* del paciente.
4. **Monitoreo pasivo por smartphone como vía escalable.** Supera al MoCA en FTD; personalización demográfica emergiendo.
5. **Edge/TinyML + Federated Learning por privacidad.** Procesamiento local como requisito, no lujo.
6. **Robots sociales con LLM.** La evidencia clínica más madura (RCTs), ahora potenciada con LLMs.
7. **Gemelos digitales cognitivos.** Aceleración fuerte desde 2023, pero sesgados a ensayos clínicos, no a asistencia diaria.

### 9.2 Tecnologías emergentes con mayor potencial 2026–2030

| Tecnología | Por qué despega | Madurez actual |
|---|---|---|
| **Memory-aware / Personalized RAG** | Personalización real paciente-específica | Emergente (TRL 3–4) |
| **Cognitive Digital Twin para asistencia diaria** | Del ensayo a la vida cotidiana | Gap abierto (TRL 3) |
| **Agentic RAG multimodal on-device** | Privacidad + razonamiento + local | Emergente (TRL 3–4) |
| **Federated Learning en red de cuidado** | Entrena sin centralizar datos sensibles | Emergente (TRL 4) |
| **Fusión voz-biomarcador + asistente agéntico** | Une detección (NeuroTrace) y acompañamiento | Casi inexistente ⚠️ |
| **Personal Knowledge Graph + Temporal RAG** | Modela trayectoria longitudinal del paciente | Emergente (TRL 3) |

---

## 10. Vacíos de investigación (research gaps) y problemas no resueltos

### 10.1 Gaps técnicos

1. **Memoria para el paciente cuya memoria falla.** Todos los sistemas de memoria de agentes asumen un usuario sano. Nadie diseñó memoria de agente que actúe como *andamio externo* de la memoria episódica degradada del paciente. **← Gap #1, altamente aprovechable.**
2. **Del gemelo digital de ensayo al gemelo de asistencia.** Los digital twins predicen progresión pero casi ninguno asiste en el día a día.
3. **Personalización socioeconómica de modelos.** El sensado pasivo empieza a incorporar "personalización demográfica", pero la integración de **cuartiles de pobreza / IDH / metadata SES** como covariables es un territorio casi virgen. **← Gap #2, tu idea original.**
4. **Alucinación en consejo médico.** Problema abierto transversal; ningún sistema lo resuelve del todo. La trazabilidad vía RAG lo mitiga pero no lo elimina.
5. **Consolidación de memoria** (qué recordar/olvidar) sin olvido catastrófico.

### 10.2 Gaps de equidad y contexto

6. **Sesgo lingüístico y dialectal.** Casi todo está en inglés; el español latinoamericano y las lenguas indígenas están subrepresentados (ver NeuroTrace).
7. **Gobernanza del agente.** ¿Para quién trabaja el asistente — paciente, cuidador o clínico? Problema no resuelto ("dynamic agent affiliation").
8. **Validación en comunidad (no institución).** La mayoría de RCTs son en centros/instituciones; falta evidencia en hogar comunitario, especialmente en LMIC.
9. **Zonas sin conectividad.** El requisito de offline/edge es reconocido pero poco resuelto en asistentes conversacionales complejos.

---

## 11. Líneas de innovación para la hackathon (enfoque Latinoamérica)

> Aquí es donde tus dos ideas convergen en propuestas concretas y defendibles.

### 11.1 Propuesta integradora: "Asistente agéntico de acompañamiento con memoria externa y personalización socioeconómica"

**Concepto núcleo:** un asistente voice-first que (a) **monitorea** biomarcadores del habla y de comportamiento de forma pasiva, (b) **acompaña** al paciente actuando como andamio de su memoria episódica, y (c) **coordina** con la red de cuidadores — todo **personalizado por contexto socioeconómico** y funcionando **on-device** para privacidad y zonas sin internet.

**Componentes y cómo cada uno ataca un gap:**

| Componente | Tecnología | Gap que ataca |
|---|---|---|
| Monitoreo pasivo de habla | Voice biomarkers (timing features) + smartphone sensing | Escalabilidad, no invasividad |
| Andamio de memoria | Personal Knowledge Graph + Temporal/Memory-aware RAG | **Gap #1** (memoria para memoria degradada) |
| Personalización SES | Metadata de cuartil de pobreza / IDH distrital como covariable | **Gap #2** (equidad socioeconómica) |
| Acompañamiento conversacional | LLM + Agentic RAG con trazabilidad (anti-alucinación) | Alucinación en consejo |
| Coordinación de cuidado | Multi-agente con roles (paciente / cuidador / clínico) | Gobernanza del agente |
| Privacidad + offline | Edge AI / TinyML + Federated Learning | Zonas sin conectividad, datos sensibles |

### 11.2 Sub-ideas defendibles por separado (por si el alcance es mucho)

1. **"Memoria externa personalizada":** PKG + Temporal RAG que le recuerda al paciente quién es cada persona que lo llama, qué hizo ayer, dónde están sus cosas — con GraphRAG sobre su vida. Alto impacto, gap claro.
2. **"Copiloto del cuidador":** Agentic RAG anclado en un grafo de conocimiento de demencia (estilo ADQueryAid) pero en **español peruano** y con recomendaciones sensibles al contexto socioeconómico de la familia.
3. **"Rutina-guardián offline":** Edge AI + sensado pasivo que aprende la rutina del paciente y alerta anomalías (wandering, inmovilidad, saltarse medicación) sin cámara ni nube — privacidad por diseño, funciona sin internet.
4. **"Gemelo cognitivo de asistencia diaria":** llevar el digital twin del ensayo clínico a la vida cotidiana — modelar la trayectoria del paciente para adaptar el nivel de apoyo del asistente.

### 11.3 Por qué esto gana en una hackathon de LatAm

- **Diferenciador socioeconómico:** nadie está personalizando estos modelos con cuartiles de pobreza/IDH. Es novedad real y socialmente relevante.
- **Offline-first:** ataca directamente la realidad de conectividad limitada en Perú/LatAm.
- **Reutiliza tu activo (NeuroTrace):** los voice biomarkers ya los tienes investigados; aquí pasan de *detección* a *acompañamiento*.
- **Base de evidencia sólida:** robots sociales y sensado pasivo tienen RCTs — puedes anclar la propuesta en evidencia, no en promesas.
- **Encaja en ODS 3** (salud y bienestar) y en el Plan Nacional de Alzheimer 2026–2028 del Perú.

---

## 12. Prioridades de lectura (si el tiempo es corto)

**Top 5 para leer primero:**
1. Digital Twin Cognition (Biomimetics 2025) — panorama completo del modelado del paciente.
2. Redefining Elderly Care with Agentic AI (arXiv 2025) — marco conceptual agéntico.
3. Multi-Agentic AI Assistant with LLM+RAG (Electronics 2026) — blueprint arquitectónico.
4. ALLFTD Mobile App (Alz & Dementia 2025) — evidencia de que lo pasivo supera al MoCA.
5. ADQueryAid (npj Biomedical Innovations 2024) — HybridRAG aplicado a cuidadores.

**Para el ángulo de memoria:** GAAMA (2026) + survey "From RAG to Agent" (2025).
**Para el ángulo SES:** el documento de integración socioeconómica de NeuroTrace + passive sensing con personalización demográfica (arXiv 2509.23158).

---

## Apéndice: nota de trazabilidad

Este documento sintetiza búsquedas de literatura realizadas en julio de 2026 sobre bases y venues prioritarios (Nature/npj, Lancet Digital Health, IEEE, ACM, Springer, Elsevier, MDPI, Frontiers, arXiv, JMIR). Los DOI e identificadores fueron tomados de las fuentes; los marcados con ⚠️ requieren verificación adicional antes de citarse en un paper formal. Los TRL son estimaciones del autor. Para el proyecto NeuroTrace (biomarcadores de habla, detección) ver el documento de estado del arte separado.
