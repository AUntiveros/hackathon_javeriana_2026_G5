# Documento maestro para la hackathon
## Ecosistema de inteligencia *aumentada* para preservar autonomía, identidad y vínculos humanos en personas con Alzheimer

> **Cuidado del adulto mayor con tecnologías emergentes (IA)**
> Documento de definición: propósito · alcance · arquitectura · hardware · papers · gaps · plan de prototipo
> Complementa a: *Revisión Sistemática de Asistentes IA para Alzheimer 2023–2026* (documento previo)

---

## 0. Cómo leer este documento

Está pensado para que el equipo salga de la lectura con tres cosas claras:

1. **El propósito** (la filosofía que nos diferencia — sección 1).
2. **El qué planeamos hacer** (la visión completa del ecosistema — secciones 2–7).
3. **El qué vamos a prototipar** (el alcance realista de la hackathon — secciones 11–14).

Cada afirmación técnica está anclada en literatura o productos reales (secciones 8–9). Los datos sin verificación plena se marcan ⚠️. Los TRL son estimaciones propias.

**Regla de oro del proyecto:** la IA no es el centro. El centro es la persona y sus vínculos. La IA es el *director de orquesta*, no el solista.

---

## 1. Propósito y filosofía — La diferencia que gana

### 1.1 El reencuadre central

La mayoría de propuestas en este espacio preguntan: *"¿Cómo hacemos una IA que cuide al paciente?"*

Nosotros preguntamos: **"¿Cómo hacemos que la IA ayude a que más personas cuiden mejor al paciente, y a que el propio paciente conserve su autonomía, identidad y relaciones el mayor tiempo posible?"**

Esto cambia todo. No construimos un chatbot. Construimos un **orquestador de la red de cuidado**.

### 1.2 Por qué esta filosofía es clínicamente correcta

Las revisiones sistemáticas coinciden: los factores que más ralentizan el deterioro no son solo tecnológicos, sino la interacción social, la actividad cognitiva y física, el propósito, la autonomía y la participación familiar. La IA **no puede reemplazar eso** — pero puede crear las condiciones para que ocurra más y mejor.

Esto se alinea con marcos establecidos: **Person-Centered Care**, envejecimiento con dignidad (*dignity-aware AI*), y medicina basada en valores.

### 1.3 Concepto propio para la hackathon: *Human-Augmented AI*

No "Human-in-the-Loop" (que ya existe y pone al humano a supervisar a la IA). Proponemos invertirlo: **Human-Augmented AI** — la IA aumenta a *toda la red de cuidado*:

- Hace que el **médico** reciba señales clínicas útiles, no solo signos vitales.
- Hace que la **familia** converse mejor (qué recordar, qué evitar, qué foto mostrar).
- Hace que el **cuidador** se agote menos (cuidador aumentado).
- Hace que los **amigos** sepan cuándo llamar.
- Hace que el **paciente** conserve más relaciones significativas.

La mejor IA aquí es **la que desaparece**: su mayor éxito no es que el paciente hable más con una máquina, sino que mantenga más tiempo las conversaciones, recuerdos y vínculos humanos que dan sentido a su vida.

### 1.4 Frase-tesis del proyecto

> *"Un ecosistema de inteligencia aumentada que preserva la identidad, la autonomía y las relaciones humanas de las personas con Alzheimer, usando la IA para fortalecer —y nunca sustituir— el vínculo entre el paciente, su familia, sus cuidadores, su comunidad y su equipo de salud."*

---

## 2. El habla como biomarcador digital central + personalización socioeconómica

> **Este es el núcleo técnico diferenciador y el puente con NeuroTrace.**

### 2.1 La innovación: conversar Y aprender clínicamente de la conversación

Casi todos los asistentes actuales **hablan** con el paciente (responden, recuerdan, acompañan), pero **muy pocos usan la conversación como fuente continua de biomarcadores digitales**. Ahí está la innovación: cada conversación diaria produce cientos de variables clínicas de forma no invasiva, barata, remota, frecuente y ecológica (captura la vida real).

### 2.2 El habla como biomarcador — por qué es tan potente

Entre 2023 y 2026 el habla se consolidó como uno de los biomarcadores digitales más prometedores en demencia. Estudios recientes muestran que las alteraciones del habla pueden aparecer **antes** que los cambios detectables por pruebas tradicionales.

**Familias de biomarcadores derivados del habla:**

| Categoría | Variables |
|---|---|
| **Prosódicos / temporales** | Velocidad, ritmo, duración y frecuencia de pausas (silenciosas y llenas), variabilidad temporal |
| **Acústicos** | Jitter, shimmer, HNR, F0, energía, MFCC, CPP |
| **Léxicos** | Riqueza léxica, TTR, MATTR, Brunet Index, Honoré Statistic |
| **Sintácticos** | Longitud media de oración, complejidad gramatical, subordinadas, profundidad sintáctica |
| **Semánticos** | Coherencia, tangencialidad, perseveración, repetición, pérdida de tópico, similitud semántica |
| **Pragmáticos** | Turn-taking, respuesta al contexto, mantenimiento del diálogo, referencia a eventos pasados |

**Modelos de fundación del habla relevantes:** Whisper, wav2vec2, HuBERT, WavLM, mHuBERT. Extraen embeddings que capturan matices prosódicos y fonéticos imposibles de detectar manualmente.

### 2.3 El problema que casi nadie estudia (nuestra oportunidad)

Los modelos actuales asumen que **todos los adultos mayores hablan "igual"**. Es falso. El habla depende de **confounders** potentes: educación, alfabetización, ocupación, idioma, dialecto, lengua materna, nivel socioeconómico, región, edad, sexo, bilingüismo, estado nutricional, depresión y aislamiento.

**Consecuencia crítica en LATAM:** no hablan igual un profesor universitario de Lima, un agricultor quechuahablante, un adulto mayor amazónico y una persona con educación primaria. Vocabulario, fluidez, sintaxis y ritmo distintos — **y eso puede confundirse con Alzheimer**, generando falsos positivos sistemáticos en poblaciones vulnerables. Un modelo entrenado con adultos mayores estadounidenses NO sirve directamente para Perú.

### 2.4 La hipótesis nueva

No modelar únicamente:

```
P(Alzheimer | Voz)
```

Sino:

```
P(Alzheimer | Voz, Contexto)
```

donde **Contexto** = nivel educativo, ingreso, índice de pobreza, IDH distrital, zona urbana/rural, idioma, lengua materna, acceso a salud, historia ocupacional, escolaridad y **reserva cognitiva**.

Esto prácticamente **no existe en la literatura**. Es novedad real y publicable.

### 2.5 Reserva cognitiva — el eje que modula todo

La **reserva cognitiva** (cognitive reserve / brain reserve / resilience) modifica cómo aparecen los síntomas: dos pacientes con el mismo daño cerebral pueden hablar completamente distinto. El modelo debería **estimar esa reserva** a partir del contexto socioeducativo, y ajustar sus umbrales en consecuencia. Es la explicación teórica de por qué la metadata socioeconómica importa: no es solo "equidad", es **exactitud**.

### 2.6 Personalización adaptativa mediante metadata

En vez de un único modelo poblacional, construir **Adaptive Personalized AI**: el agente conoce educación, historial, rutina, ocupación, familia, personalidad, humor, religión, costumbres, idioma y dialecto — y adapta tanto las conversaciones como las alertas como la interpretación de los biomarcadores.

---

## 3. Conversación terapéutica — del monitoreo al acompañamiento activo

> Aquí cerramos el ciclo donde casi todos los papers se quedan cortos: **ellos monitorean, no intervienen.**

### 3.1 La evidencia más fuerte: conversar retrasa el deterioro (I-CONECT)

El ensayo clínico **I-CONECT** demostró que **conversaciones semi-estructuradas y cognitivamente estimulantes** son una estrategia efectiva para combatir el aislamiento social y el deterioro cognitivo en adultos mayores con MCI. Su limitación para escalar: dependía de entrevistadores humanos entrenados. El sistema **AI-CONECT** (2025–2026) implementa ese protocolo con LLMs, con marco de "IA responsable" y evaluación mediante "usuarios virtuales" (réplicas IA de participantes con MCI y cognición normal).

**Implicación para nosotros:** la conversación diaria no es solo acompañamiento — es una **intervención no farmacológica con base de evidencia** para preservar función cognitiva.

### 3.2 El loop cerrado de retroalimentación

```
Conversación
   ↓
Extracción de biomarcadores
   ↓
Actualización del Gemelo Cognitivo
   ↓
Predicción del deterioro
   ↓
Personalización
   ↓
Nueva conversación terapéutica (ejercita funciones)
   ↓
Nuevos biomarcadores
   ↓
Aprendizaje continuo
```

### 3.3 Conversaciones que ejercitan funciones cognitivas específicas

| Función cognitiva | Ejemplo de prompt conversacional |
|---|---|
| Memoria episódica | "¿Qué hiciste ayer?" |
| Memoria autobiográfica | "Cuéntame cómo conociste a tu esposa." |
| Orientación temporal | "¿Qué día es hoy?" |
| Orientación espacial | "¿Dónde estamos?" |
| Lenguaje | "Descríbeme esta imagen." (← tarea Cookie Theft) |
| Funciones ejecutivas | "¿Qué harías si se corta la luz?" |
| Atención | "Juguemos a las veinte preguntas." |
| Reminiscencia | Mostrar fotografías familiares y conversar. |
| Musicoterapia | Hablar sobre canciones conocidas. |
| Narración | Crear historias juntos. |

### 3.4 Terapias no farmacológicas con evidencia que podemos digitalizar

- **Cognitive Stimulation Therapy (CST):** recomendada por NICE (Reino Unido); puede ser aplicada por personal no especializado. RCT clásico de Spector et al. (2003) muestra eficacia.
- **Reminiscence Therapy (RT):** una de las intervenciones psicosociales más usadas en etapas temprana-media; estimula memoria, mejora ánimo y fortalece identidad. Revisiones 2025–2026 exploran su potenciación con IA generativa (Rememo, Remihaven, AI-generada personalización).
- **Cognitive rehabilitation vía voice agent:** Moneta Health entrega rehabilitación cognitiva por agente de voz telefónico, revisada por fonoaudiólogo (SLP); cohorte de 75 pacientes (edad media 73, MoCA medio 20; 59% MCI, 33% demencia).

⚠️ **Nota importante de gap:** solo ~30% de los estudios de RT involucran explícitamente a los *facilitadores* (cuidadores/terapeutas), pese a su rol central. Diseñar *para y con* ellos es una oportunidad diferenciadora.

---

## 4. Gemelo Digital Cognitivo + Social Digital Twin

### 4.1 Gemelo Digital Cognitivo (del paciente)

No solo guardar historial: construir un **modelo dinámico** que integra múltiples fuentes:

```
Paciente
  ├── Speech biomarkers
  ├── Smartphone (uso, tipeo, movilidad)
  ├── Wearables (FC, HRV, actividad)
  ├── Sueño
  ├── Rutinas / GPS
  └── Interacciones sociales
        ↓
  Gemelo Digital Cognitivo
        ↓
  Estima: estado cognitivo · estado emocional · riesgo · fatiga ·
          progresión · adherencia · carga del cuidador · nivel de autonomía
```

**Estado del arte:** revisión sistemática PRISMA de 78 estudios (2017–2025) muestra aceleración fuerte desde 2023. Pero **la mayoría se orienta a ensayos clínicos y predicción de progresión, no a asistencia diaria** — ahí está nuestro gap de aplicación.

### 4.2 Social Digital Twin (de la red) — idea propia poco explorada

No solo modelar al paciente: **modelar su red social**. Quién es importante, quién dejó de visitarlo, quién lo llama más, quién genera bienestar, quién lo estresa, qué conversaciones le hacen bien, qué actividades disfruta con cada persona. La IA optimiza **la red social**, no solo la cognición.

### 4.3 Digital Home Twin (del hogar) — idea propia

Modelar también la casa: habitaciones, objetos, medicamentos, sensores, rutinas y eventos. Así la IA entiende el **contexto**, no solo a la persona. Útil para memoria espacial aumentada (ver §6.7).

---

## 5. Arquitectura del sistema integral

### 5.1 Los cuatro módulos que se retroalimentan

```
┌─────────────────────────────────────────────────────────┐
│  1. MONITOREO CONTINUO NO INVASIVO                        │
│     Biomarcadores del habla (ES-LATAM) + datos pasivos    │
│     del smartphone (actividad, movilidad, sueño, uso)     │
└───────────────────────────┬─────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  2. GEMELO DIGITAL COGNITIVO                              │
│     Integra biomarcadores + historia + rutinas +          │
│     contexto social + evolución longitudinal              │
│     → estima riesgo y nivel de autonomía                  │
└───────────────────────────┬─────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  3. ASISTENTE AGÉNTICO CON MEMORIA                       │
│     Multi-agent + Memory-aware GraphRAG + Personal        │
│     Knowledge Graph → recuerda eventos, adapta            │
│     conversaciones, propone ejercicios, coordina red      │
└───────────────────────────┬─────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  4. MOTOR DE PERSONALIZACIÓN SOCIOECONÓMICA              │
│     Escolaridad, reserva cognitiva, idioma, dialecto,     │
│     índice de pobreza, zona, acceso a salud → reduce      │
│     sesgo y da recomendaciones culturalmente pertinentes  │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Stack técnico propuesto (visión completa)

```
Paciente
   ↓
Voice Companion (voice-first)
   ↓
Speech Foundation Model (Whisper / wav2vec2 / HuBERT)
   ↓
Extracción de biomarcadores (prosódicos, acústicos, léxicos, sintácticos, semánticos, pragmáticos)
   ↓
Gemelo Digital Cognitivo  ←──── Motor de personalización socioeconómica
   ↓
Personal Knowledge Graph
   ↓
Memory-aware GraphRAG
   ↓
LLM Agéntico (orquestador)
   ↓
Multi-agent: [Paciente] [Cuidador] [Médico] [Familiar] [Comunidad]
   ↓
Alertas · Recomendaciones · Ejercicios cognitivos · Conexiones humanas
   ↓
Aprendizaje continuo → (vuelve al Voice Companion)
```

**Nota arquitectónica:** este patrón (orquestador + agentes especializados + RAG + trazabilidad anti-alucinación) es el estándar 2025–2026, con blueprint casi directo en el paper de asistente multi-agente médico (Electronics 2026, LangChain + LangGraph + Gemini 2.5 Flash).

---

## 6. Ecosistema de hardware multimodal

> La IA es el cerebro. El producto ganador es la **combinación de sensores, interfaces y agentes**. Cada componente ataca un problema que la voz sola no puede resolver.

### 6.1 Smartphone — el cerebro principal
Corre el LLM/orquestador (o se conecta a él), el GraphRAG y el Gemelo Cognitivo. Sensado pasivo: actividad, movilidad (GPS), tipeo, uso del dispositivo, sueño. **Es lo mínimo indispensable y lo más escalable.**

### 6.2 Smart glasses (la apuesta con más momentum 2025–2026)
Permiten que la IA "vea" el mundo desde la perspectiva del paciente. Funciones: reconocer familiares y mostrar nombre/relación, identificar objetos, instrucciones paso a paso (cocinar, vestirse), guía ante desorientación, leer etiquetas de medicamentos, detectar riesgos (estufa, puerta), construir un **Life Log** que alimenta el Gemelo. No hace falta fabricar hardware: se puede desarrollar sobre Ray-Ban Meta, Android XR, Rokid, etc. (ya traen cámara, micrófonos, altavoces, IA conversacional). Ver productos reales en §9.

### 6.3 Smartwatch / wearables
Aportan lo que la voz nunca medirá: frecuencia cardíaca, HRV, actividad física, caídas, sueño, sedentarismo, estrés, adherencia a caminatas. Sirven como recordatorios por vibración, botón SOS, confirmación de medicación. Pilar de los biomarcadores digitales en Alzheimer.

### 6.4 Cámara ambiental (con Edge AI obligatorio)
Detecta caídas, wandering, cocinar, comer, tomar medicamentos, uso del baño, tiempo sentado. **Problema de privacidad → la tendencia es Edge AI**: todo se procesa localmente, nunca se sube video, solo se generan *eventos* ("09:30 desayunó", "14:00 no salió del dormitorio").

### 6.5 Etiquetas inteligentes (localización de objetos)
- **QR:** las gafas lo leen → "este es tu inhalador".
- **NFC:** acercar el reloj → reconoce el objeto.
- **UWB / Bluetooth (tipo AirTag):** "¿dónde están mis lentes?" → "a tu izquierda, sobre la mesa". Ideal para llaves, billetera, medicamentos.

### 6.6 Casa inteligente (IoT) — interactuar, no solo monitorear
Apagar cocina si el paciente sale, cerrar puerta, encender luces nocturnas, detectar humo/gas. Seguridad activa.

### 6.7 Memoria espacial aumentada (la idea más innovadora — casi inédita)
Las gafas construyen un mapa 3D de la casa (SLAM) y la IA recuerda **dónde quedaron las cosas**. "¿Dónde dejé mis lentes?" → "Hace una hora los dejaste sobre la mesa del comedor." No busca en internet: busca en su **propia memoria visual**. Combina visión por computadora + SLAM + memoria episódica + GraphRAG + LLM + Digital Twin. **No hemos visto casi nada igual en la literatura.**

### 6.8 Otros
Auriculares inteligentes (discretos, siempre disponibles), robot social/mascota (evidencia RCT — §8 doc previo), hardware biomédico Bluetooth (tensiómetro, oxímetro, glucómetro, ECG portátil, balanza) alimentando el mismo Gemelo. Diferenciador para un equipo biomédico.

---

## 7. El factor humano — la IA como director de orquesta

> No es el violín ni el piano. Es el **director**. Los protagonistas son los músicos: paciente, familia, amigos, médicos, cuidadores, comunidad.

### 7.1 El objetivo deja de ser "conversar" y pasa a ser "crear conversaciones humanas"

Ejemplo: la IA detecta que el paciente lleva 3 días sin hablar con su nieta. **No llama ella.** Sugiere: *"Hoy sería buen día para llamar a Sofía"* y prepara el contexto: *"La última vez hablaron del cumpleaños de tu bisnieto."* La conversación ocurre entre humanos. **La IA desaparece.**

### 7.2 El cuidador aumentado (efecto multiplicador)

La IA no conversa por el cuidador — hace que el cuidador converse mejor: qué preguntar, qué evitar, cuándo intervenir, qué emociones observar, qué recuerdos estimular, qué música funciona. Se apoya en la evidencia de CST y RT aplicables por no especialistas.

### 7.3 La IA como generadora de comunidad

Conectar personas: dos adultos mayores que fueron profesores → la IA detecta intereses comunes y sugiere una videollamada o encuentro. Combate el aislamiento (factor de riesgo directo de demencia).

### 7.4 Señales clínicas útiles para el médico (no solo signos vitales)

En vez de solo FC/peso/presión, el médico recibe: *"En 3 semanas subió 25% la repetición de preguntas"*, *"disminuyó la riqueza léxica"*, *"dejó de mencionar espontáneamente a su esposa"*, *"redujo 40% las conversaciones con familiares"*. Muchísimo más accionable — y todo derivado de los biomarcadores del habla + sensado pasivo.

### 7.5 IA como entrenador social

Misiones diarias humanas, no digitales: *"Hable con alguien 15 minutos"*, *"Cuéntele una historia de su infancia a su nieto"*, *"Salga a caminar con un vecino."*

### 7.6 Diagrama del paradigma

```
              Médico
                ▲
                │
Familia ◄──── IA ────► Cuidador
                │
                ▼
            Comunidad
                │
                ▼
             Paciente
```

La IA **conecta**. No reemplaza.

---

## 8. Catálogo ampliado de papers, reviews y patentes (nuevos, 2025–2026)

> Complementa las 15 fichas del documento previo. Foco en habla-biomarcador, conversación terapéutica y hardware.

### Habla como biomarcador y personalización
- **Assistive Intelligence: A Framework for AI-Powered Technologies Across the Dementia Continuum.** *AI (MDPI)* 6(1):8, ene 2026. DOI 10.3390/ai6010008 ⚠️. Marco que alinea IA (generativa, NLP, sensado) con cada etapa (preclínica, leve, moderada, severa). **TRL:** conceptual. **Uso:** justifica la visión por etapas.
- **Language-Based Digital Twins for Elderly Cognitive Assistance.** *arXiv*:2606.27334, 2026. Gemelo basado en lenguaje; critica que el campo se centra en predicción y no en asistencia. **Puente directo habla → asistente.**
- **Evaluating spoken language as a biomarker for automated screening of cognitive impairment.** *Communications Medicine* (Nature), 2025 (Geranmayeh, Barnaghi et al.). Habla espontánea como screening. **TRL 4–5.**

### Conversación terapéutica / estimulación cognitiva (evidencia clave)
- **AI-CONECT: Designing Responsible-AI-based Conversational Chatbots for Dementia Intervention.** PMC12763565, 2025–2026. Implementa el protocolo I-CONECT con LLMs; usuarios virtuales para evaluación. **TRL 4.** **← El más importante: evidencia de que conversar retrasa deterioro.**
- **A Principle-Driven Adaptive Policy for Group Cognitive Stimulation Dialogue.** *arXiv*:2603.10034, 2026. Política adaptativa para diálogo de estimulación cognitiva grupal. **TRL 3.**
- **Rememo: AI-in-the-loop Therapist's Tool for Dementia Reminiscence.** *arXiv*:2602.17083, 2026. Research-through-design; señala el gap de involucrar a facilitadores.
- **AI in Reminiscence Therapy for Older Adults: Systematic Review Protocol.** *medRxiv* 2025.09.21, 2025. Protocolo PRISMA-P.
- **Improving Access to Dementia Care through AI-Powered Cognitive Rehabilitation (Moneta Health).** *Alzheimer's & Dementia* 21(S4):e098721, dic 2025. Voice agent + SLP, n=75. **TRL 6 (producto real).**
- **Barriers and Facilitators to Implementing CST and Reminiscence Therapy in Care Homes.** *Int J Geriatr Psychiatry*, DOI 10.1002/gps.70124, jul 2025. Revisión de implementación (NICE-recomendadas, aplicables por no especialistas).

### Hardware — smart glasses (prototipables)
- **Smart Glasses for Facial Recognition and Memory Assistance in Alzheimer's care.** George et al., *Alzheimer's & Dementia* 21:e103276, dic 2025. DOI 10.1002/alz70858_103276. **ESP32-CAM + OpenCV/dlib + TTS + GPS.** Firmware en C. **← Prototipable con hardware barato. TRL 4.**
- **Smart Glasses and Virtual Assistance Guide for Detection of Disorientation.** Sharma et al., Springer 2025. Gafas con SIM + sensores + asistente AR para guiar al paciente desorientado a lugar seguro.
- **Advanced augmented assistive device for dementia (PATENTE US 12,191,035).** USPTO. Gafas AR con reconocimiento facial (VGG-Face/FaceNet/ArcFace) + reconocimiento de emociones + comprensión contextual; muestran nombre, relación, última interacción y recuerdos compartidos. **← Revisar para libertad de operación.**
- **Social Assistance System for AR to Redound Face Blindness with 3D Face Recognition.** *Electronics* 14(7):1244, 2025. DOI 10.3390/electronics14071244.

### Sensado y edge (contexto)
- **Human-Centered Ambient and Wearable Sensing for Automated Monitoring in Dementia Care: Scoping Review.** *arXiv*:2603.05516, 2026. Mapa completo de modalidades. Señala el gap de "dynamic agent affiliation".
- **Digital biomarkers for brain health: passive and continuous assessment from wearable sensors.** *npj Digital Medicine*, DOI 10.1038/s41746-026-02340-y, ene 2026. n=82, 21 outcomes.
- **Smartwatch- and smartphone-based remote assessment of brain health and detection of MCI.** *Nature Medicine*, 2025 (Butler et al.).

---

## 9. Productos comerciales y benchmarking de mercado

| Producto | Qué hace | Hardware | Estado | Gap que deja |
|---|---|---|---|---|
| **CareYaya — MedaCareLLM** | Gafas IA con reconocimiento facial y de objetos, asistencia en tiempo real | Smart glasses | Anunciado 2024 ⚠️ | No en español LATAM; no personalización SES |
| **CrossSense — "Wispy"** (Animorph, Longitude Prize) | Gafas AR + app; el usuario asigna etiquetas de texto/audio a objetos; **edge server offline, sin nube** | Smart glasses + caja edge | Testing 15–30 PLWD + carers, 2025 | Foco UK; no monitoreo de biomarcadores del habla |
| **Ray-Ban Meta / Rokid / Android XR** | Gafas IA de consumo (cámara, mic, altavoz, IA conversacional) | Smart glasses comerciales | En mercado | Falta la capa biomédica especializada ← **nuestra oportunidad** |
| **Moneta Health** | Rehabilitación cognitiva por voice agent + SLP humano | Teléfono | Producto, n=75 | Inglés; no multimodal; no metadata SES |
| **PARO / robot PIO** | Robot social terapéutico (RCTs positivos) | Robot | Comercial / investigación | Costoso; no monitoreo longitudinal integrado |
| **CrossSense won $1.4M Longitude Prize on Dementia (2026)** | Valida el interés global y el enfoque assistive-tech + independencia | — | Premio 2026 | Confirma que el mercado se mueve hacia esto |

**Lectura de mercado:** el mundo se mueve hacia gafas asistivas y herramientas de independencia cotidiana. **Ninguno** combina (a) biomarcadores del habla como monitoreo longitudinal, (b) personalización socioeconómica LATAM, (c) orquestación de la red humana, y (d) español peruano con dialectos. **Ese cruce es nuestro espacio en blanco.**

---

## 10. Gaps de mercado e investigación (resumen accionable)

| # | Gap | Por qué importa | Quién lo ataca hoy |
|---|---|---|---|
| 1 | **P(AD \| Voz, Contexto socioeconómico)** en español LATAM | Exactitud + equidad; evita falsos positivos en analfabetos/baja escolaridad | Casi nadie |
| 2 | **Memoria de agente para memoria degradada** (andamio externo) | Los sistemas de memoria asumen usuario sano | Nadie específicamente |
| 3 | **Del Digital Twin de ensayo al de asistencia diaria** | Los gemelos predicen progresión, no asisten | Muy pocos |
| 4 | **Conversación como fuente continua de biomarcadores** (no solo compañía) | Cierra el loop monitoreo↔intervención | Emergente (I-CONECT) |
| 5 | **Involucrar a facilitadores/cuidadores en el diseño** de RT/CST | Solo ~30% de estudios lo hace | Gap señalado |
| 6 | **Memoria espacial aumentada** (dónde quedaron las cosas) | Autonomía real en el hogar | Casi inédito |
| 7 | **Social Digital Twin** (modelar la red, no solo la persona) | Optimiza vínculos, no solo cognición | Inédito ⚠️ |
| 8 | **Orquestación humana / Human-Augmented AI** | La IA como director, no solista | Conceptual |
| 9 | **Offline-first en zonas sin conectividad** | Realidad de Perú/LATAM | Edge emergente |
| 10 | **Español peruano + dialectos + quechua** | Nadie tiene datasets ni modelos | Inexistente |

---

## 11. Alcance para la hackathon — Qué haremos vs qué prototiparemos vs futuro

> Diferenciar el **alcance potencial (visión)** del **alcance prototipable (hackathon)** es clave para no prometer de más y ejecutar bien.

### 11.1 Tres capas de alcance

**CAPA A — Prototipable en la hackathon (comprometido):**
- ✅ **Entrenamiento de modelos NLP/LLM** para evaluar performance en español + análisis del efecto de la metadata (escolaridad, zona, IDH) sobre los biomarcadores del habla.
- ✅ **App / chatbot con asistentes de IA con personalidades por rol** (paciente, cuidador, familiar, médico, comunidad).
- ✅ **Pipeline de biomarcadores del habla** (Whisper + features prosódicas/léxicas) sobre datasets Cookie Theft en español.
- ✅ **Conversaciones terapéuticas** que ejercitan funciones cognitivas (prompts estructurados estilo I-CONECT/CST).
- ✅ **Gemelo Cognitivo mínimo**: dashboard que integra biomarcadores + eventos + tendencia longitudinal (aunque sea con datos simulados/semilla).
- ✅ **Hardware básico prototipable**: smartwatch con ESP32 (o similar) para FC/actividad/pasos/botón SOS; recordatorios por vibración.
- ✅ **Smart tags** para localización de objetos (NFC/QR/BLE) **si conseguimos alguno**.
- ✅ **Motor de personalización socioeconómica** (aunque sea reglas + covariable en el modelo).

**CAPA B — Demo conceptual / mock (mostrar la visión, no producción):**
- 🔶 Panel del médico con señales clínicas derivadas del habla.
- 🔶 Orquestación de la red humana (sugerencias de "llama a tu nieta").
- 🔶 Edge AI para privacidad (mencionar arquitectura, mock del flujo de eventos).

**CAPA C — Futuro / roadmap (declarado, no prototipado):**
- 🔷 Integración de **smart home** (control de gas, puertas, luces).
- 🔷 **Visión artificial con smart glasses** (reconocimiento facial/objetos, memoria espacial aumentada).
- 🔷 Múltiples **sensores paramétricos biomédicos** (oxímetro, tensiómetro, ECG).
- 🔷 Cámara ambiental con detección de ADL/caídas.
- 🔷 Social Digital Twin completo y Digital Home Twin.

### 11.2 Recomendación de foco para maximizar impacto/esfuerzo

**Núcleo demostrable = Capa A, priorizando:**
1. El **pipeline de habla + metadata socioeconómica** (es el diferenciador y lo publicable).
2. El **chatbot multi-rol con conversación terapéutica** (es lo tangible y emotivo para el jurado).
3. El **Gemelo Cognitivo mínimo** como pegamento visual que une todo.
4. Un **hardware simbólico** (smartwatch ESP32 o smart tag) para mostrar que es multimodal y real.

Todo lo demás se presenta como **roadmap creíble** con papers y productos que lo respaldan (secciones 8–9).

---

## 12. Datasets y plan técnico

### 12.1 Datasets Cookie Theft en español (con metadata) — el activo clave

- **Ivanova Corpus (DementiaBank, España):** 361 sujetos (74 AD, 90 MCI, 197 HC), Cookie Theft + lectura. Incluye nivel educativo en metadata. Acceso: membresía TalkBank (talkbank@cmu.edu).
- **PerLA Corpus (España):** foco pragmático.
- **MultiConAD:** unifica 16 datasets (inglés, español, chino, griego); disponible en HuggingFace.
- **Idea central del paper/hackathon:** tomar modelos que hoy solo existen bien en inglés y chino, medir su performance en español, y **cuantificar cuánto mejora al añadir metadata socioeconómica/reserva cognitiva** como covariable. Nadie lo ha hecho sistemáticamente.

### 12.2 Plan técnico mínimo (Capa A)

```
1. Acceso a Ivanova Corpus (TalkBank) — solicitar YA (2–5 días).
2. Pipeline: Whisper (transcripción) → features (librosa: MFCC/F0/jitter/shimmer;
   spaCy es: TTR/sintaxis; pausas: webrtcvad).
3. Modelos: RF / SVM / XGBoost. Baseline sin metadata vs con metadata (educación, zona, IDH).
4. Métrica: AUC + sensibilidad/especificidad ESTRATIFICADAS por nivel educativo (fairness).
5. Chatbot: LLM + prompts terapéuticos por función cognitiva + personalidades por rol.
6. Gemelo mínimo: dashboard (biomarcadores + tendencia + alertas) — datos semilla si hace falta.
7. Hardware: ESP32 + sensor FC/IMU → app (BLE) → recordatorios/SOS.
```

### 12.3 Deploy
- Entrenamiento de modelos: ✅ factible (Colab/local).
- Deploy de apps: ✅ factible (móvil/web).
- Hardware básico ESP32/smartwatch: ✅ factible.
- Smart tags: ✅ si conseguimos hardware.

---

## 13. Roles de personalidad de IA (multi-agente)

Chatbots/asistentes con **personalidades basadas en rol**, cada uno con objetivos, tono y datos distintos:

| Rol | Objetivo del agente | Tono | Qué NO hace |
|---|---|---|---|
| **Agente Paciente** | Acompañar, estimular cognición, extraer biomarcadores, preservar identidad | Cálido, paciente, culturalmente pertinente (dialecto) | No dar diagnóstico ni alarmar |
| **Agente Cuidador** | Cuidador aumentado: qué preguntar/evitar, alertas, reducir carga | Práctico, empático, orientado a acción | No reemplazar el juicio del cuidador |
| **Agente Familiar** | Sugerir contacto, preparar contexto de conversación, reminiscencia | Cercano, motivador | No invadir privacidad del paciente |
| **Agente Médico** | Resumir señales clínicas del habla + sensado, trazabilidad | Técnico, conciso, con fuentes | No sustituir decisión clínica |
| **Agente Comunidad** | Conectar pares con intereses comunes, generar red | Social, inclusivo | No exponer datos sensibles |

**Clave de seguridad:** todos anclados en RAG con trazabilidad para mitigar alucinaciones; ninguno emite consejo médico no verificado.

---

## 14. Requisitos y checklist para arrancar

### 14.1 Definición del propósito (para el pitch)
- [ ] Frase-tesis memorizada (§1.4).
- [ ] Concepto *Human-Augmented AI* como diferenciador (§1.3).
- [ ] Historia de impacto: caso de un adulto mayor quechuahablante mal clasificado por un modelo gringo.

### 14.2 Qué planeamos hacer (visión)
- [ ] Ecosistema de 4 módulos (§5.1).
- [ ] Roadmap de hardware por capas (§11.1).
- [ ] Gaps que atacamos, con papers de respaldo (§10).

### 14.3 Qué vamos a prototipar (Capa A)
- [ ] Pipeline habla + metadata socioeconómica sobre Cookie Theft español.
- [ ] Chatbot multi-rol con conversación terapéutica.
- [ ] Gemelo Cognitivo mínimo (dashboard).
- [ ] Hardware simbólico (ESP32/smartwatch o smart tag).

### 14.4 Riesgos y mitigaciones
- [ ] Acceso a dataset a tiempo → solicitar TalkBank el día 1; tener plan B con MultiConAD (HuggingFace, sin gestión).
- [ ] Alucinación del LLM → RAG con trazabilidad + reglas de formato + disclaimers.
- [ ] Privacidad → edge-first en el discurso; datos sensibles nunca a la nube en el mock.
- [ ] Sobre-alcance → separar claramente Capa A (se entrega) de C (roadmap).

### 14.5 Ética y encuadre
- [ ] La IA **no diagnostica** — alerta y acompaña; la decisión es del médico.
- [ ] Person-Centered Care y dignidad como principios rectores.
- [ ] Consentimiento informado y protección de datos (Ley N° 29733 Perú).
- [ ] Alineación con ODS 3 y Plan Nacional de Alzheimer 2026–2028 (Perú).

---

## Apéndice — Prioridades de lectura (top 8 nuevos)

1. **AI-CONECT** (PMC12763565) — evidencia de que conversar retrasa el deterioro.
2. **Assistive Intelligence Framework** (AI/MDPI 2026) — IA por etapas de demencia.
3. **Smart Glasses ESP32-CAM** (Alz & Dementia 2025) — prototipo de hardware barato.
4. **Language-Based Digital Twins** (arXiv 2606.27334) — puente habla↔asistente.
5. **Human-Centered Ambient Sensing scoping review** (arXiv 2603.05516) — mapa de sensado + gap de gobernanza del agente.
6. **Digital Twin Cognition** (Biomimetics 2025) — panorama de modelado del paciente.
7. **CrossSense / Longitude Prize** — producto edge-offline de referencia.
8. **Patente US 12,191,035** — gafas AR con reconocimiento facial + emocional (libertad de operación).

---

*Documento vivo. Los datos marcados ⚠️ requieren verificación antes de cita formal; los TRL son estimaciones propias. Búsquedas realizadas en julio 2026 sobre Nature/npj, Lancet Digital Health, IEEE, ACM, Springer, Elsevier, MDPI, Frontiers, arXiv, JMIR, USPTO. Complementa el documento previo de estado del arte y el de NeuroTrace (biomarcadores del habla).*
