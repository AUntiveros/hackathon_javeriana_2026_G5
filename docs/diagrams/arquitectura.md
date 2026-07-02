# Diagramas de arquitectura — Ecosistema Alzheimer

Todos en Mermaid. Render en GitHub, VS Code (extensión Markdown Preview Mermaid) o mermaid.live.

---

## 1. C4 Nivel 1 — Contexto

```mermaid
graph TB
    subgraph Personas["Red de cuidado (Human-Augmented AI)"]
        PAC["👴 Paciente<br/>(Alzheimer)"]
        CUI["🧑‍⚕️ Cuidador"]
        MED["👨‍⚕️ Médico /<br/>personal de salud"]
        FAM["👨‍👩‍👧 Familiar"]
        COM["🌐 Comunidad /<br/>red de apoyo"]
    end

    SIS["🎼 ECOSISTEMA IA<br/>Orquestador de la red de cuidado<br/>(el 'director de orquesta')"]

    GEM["☁️ Gemini 2.5 Flash<br/>(LLM comercial)"]
    HW["⌚ Wearable ESP32<br/>(FC, pasos, SOS)"]

    PAC -->|conversa por voz| SIS
    SIS -->|acompaña, recuerda, estimula| PAC
    CUI -->|gestiona tareas, ve alertas| SIS
    SIS -->|alertas, plan, coaching| CUI
    MED -->|ajusta terapia, ve reportes| SIS
    SIS -->|señales clínicas del habla| MED
    FAM -->|recibe sugerencias| SIS
    SIS -->|"llama a tu nieta Sofía"| FAM
    COM -->|matching de pares| SIS
    SIS -->|conecta intereses comunes| COM

    SIS <-->|razonamiento LLM| GEM
    HW -->|biométricos BLE| SIS
    SIS -->|recordatorio, vibración| HW
```

---

## 2. C4 Nivel 2 — Contenedores

```mermaid
graph TB
    subgraph Front["FRONTEND (React + Vite, voice-first)"]
        UIP["Vista Paciente<br/>(chat de voz)"]
        UIC["Vista Cuidador"]
        UIM["Vista Médico"]
        UIF["Vista Familiar"]
        UICom["Vista Comunidad"]
        DASH["📊 Dashboard<br/>Gemelo Cognitivo"]
    end

    subgraph Back["BACKEND (FastAPI)"]
        ORQ["🎼 Orquestador<br/>(LangGraph)<br/>Role Router = RBAC"]
        RAG["🔎 Servicio RAG<br/>(ChromaDB + PKG)"]
        SES["⚖️ SES Personalizer"]
        RUT["📅 Motor de rutina<br/>(orquestación día-a-día)"]
        BIO["🎙️ Servicio Biomarcadores<br/>Whisper→features→modelo"]
        DB[("🗄️ SQLite<br/>paciente, eventos,<br/>twin, biomarcadores")]
    end

    GEM["☁️ Gemini 2.5 Flash"]
    HW["⌚ ESP32"]

    UIP & UIC & UIM & UIF & UICom -->|REST / WS| ORQ
    DASH -->|REST| DB
    DASH -->|REST| BIO
    ORQ --> RAG
    ORQ --> SES
    ORQ --> RUT
    ORQ -->|function calling| GEM
    ORQ --> DB
    RUT --> DB
    BIO --> DB
    BIO -.->|riesgo alimenta| DASH
    HW <-->|Web Bluetooth| UIC
    HW -->|biométricos| DB
```

---

## 3. C4 Nivel 3 — Componentes del Orquestador (RBAC)

```mermaid
graph TB
    IN["Entrada del usuario<br/>+ rol autenticado"]
    ROUTER{"Role Router<br/>(RBAC)"}

    subgraph Agentes["Agentes especializados por rol"]
        AP["Agente Paciente<br/>tono cálido"]
        AC["Agente Cuidador<br/>práctico"]
        AM["Agente Médico<br/>técnico + fuentes"]
        AF["Agente Familiar<br/>cercano"]
        ACom["Agente Comunidad<br/>social"]
    end

    subgraph Herramientas["Tools (function calling)"]
        T1["consultar_PKG"]
        T2["log_medicacion"]
        T3["agendar_actividad"]
        T4["extraer_biomarcador"]
        T5["reporte_clinico"]
        T6["sugerir_contacto"]
    end

    GUARD["🛡️ Guardrails<br/>formato + disclaimers<br/>anti-alucinación"]
    MEM["🧠 Memory Manager<br/>(scope por rol)"]

    IN --> ROUTER
    ROUTER -->|rol=paciente| AP
    ROUTER -->|rol=cuidador| AC
    ROUTER -->|rol=medico| AM
    ROUTER -->|rol=familiar| AF
    ROUTER -->|rol=comunidad| ACom

    AP --> T1 & T4
    AC --> T2 & T3
    AM --> T5
    AF --> T6
    ACom --> T6

    AP & AC & AM & AF & ACom --> MEM
    AP & AC & AM & AF & ACom --> GUARD
    GUARD --> OUT["Respuesta trazable"]
```

---

## 4. Loop cerrado — conversación como biomarcador (núcleo diferenciador)

```mermaid
flowchart LR
    A["🗣️ Conversación<br/>terapéutica diaria"] --> B["🎙️ Extracción de<br/>biomarcadores del habla"]
    B --> C["🧠 Actualización del<br/>Gemelo Cognitivo"]
    C --> D["📈 Predicción de<br/>deterioro / riesgo"]
    D --> E["⚖️ Personalización<br/>(SES + reserva cognitiva)"]
    E --> F["🎯 Nueva conversación<br/>que ejercita funciones"]
    F --> A
    B -.->|features| G[("Biomarker store")]
    C -.->|snapshot| H[("Twin store")]
    D -.->|alerta si supera umbral| I["🚨 Escalado al cuidador"]
```

---

## 5. ⭐ Orquestación del día-a-día del paciente (requerido)

Secuencia de un día típico gestionado por el Motor de Rutina + agentes.

```mermaid
sequenceDiagram
    autonumber
    participant R as 📅 Motor de Rutina
    participant AP as 🤖 Agente Paciente
    participant P as 👴 Paciente
    participant HW as ⌚ ESP32
    participant T as 🧠 Gemelo Cognitivo
    participant AC as 🧑‍⚕️ Agente Cuidador
    participant C as Cuidador

    Note over R: 08:00 — Inicio del día
    R->>AP: Trigger rutina matutina
    AP->>P: "Buenos días Don José.<br/>¿Cómo durmió?" (check-in de voz)
    P-->>AP: (responde por voz)
    AP->>T: extraer_biomarcador(audio)
    AP->>P: Orientación temporal:<br/>"Hoy es jueves 2 de julio"

    Note over R: 08:30 — Medicación
    R->>AP: Recordatorio medicación
    AP->>P: "Es hora de su pastilla azul"
    HW-->>P: vibra (recordatorio háptico)
    P-->>AP: "Ya la tomé"
    AP->>T: log_medicacion(tomada=true)

    Note over R: 10:00 — Actividad NO repetitiva
    R->>R: elegir_actividad(historial,<br/>intereses, no-repetir)
    R->>AP: Proponer actividad
    AP->>P: "¿Le gustaría ver fotos<br/>de su boda?" (reminiscencia)
    AP->>T: registrar engagement

    Note over R: 13:00 — Monitoreo pasivo
    HW->>T: FC, pasos, actividad
    T->>T: evaluar riesgo/autonomía

    Note over R: 15:00 — Detección de anomalía
    HW->>T: sedentarismo prolongado
    T->>AC: riesgo elevado
    AC->>C: "Don José lleva 3h sin<br/>moverse. ¿Todo bien?"

    Note over R: 18:00 — Conexión humana
    T->>AC: 3 días sin hablar con nieta
    AC->>C: "Buen día para que Sofía<br/>lo llame. Último tema:<br/>cumpleaños del bisnieto"

    Note over R: 20:00 — Cierre + adherencia
    R->>T: consolidar_dia()
    T->>AC: resumen: adherencia 100%,<br/>ánimo estable, léxico normal
```

---

## 6. Máquina de estados del wearable ESP32

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Midiendo: cada 30s
    Midiendo --> Idle: publica FC/pasos (BLE)
    Idle --> Recordatorio: recibe cmd BLE
    Recordatorio --> Vibrando: activa motor
    Vibrando --> Idle: confirmado / timeout
    Idle --> SOS: botón presionado 3s
    SOS --> AlertaEnviada: notifica cuidador
    AlertaEnviada --> Idle: reconocido
```

---

## 7. Despliegue (hackathon)

```mermaid
graph TB
    subgraph Laptop["💻 Laptop dev (demo local)"]
        FE["Frontend Vite<br/>localhost:5173"]
        BE["FastAPI<br/>localhost:8000"]
        CH[("ChromaDB<br/>local")]
        SQ[("SQLite")]
    end

    subgraph Colab["☁️ Google Colab / HF Space"]
        TRAIN["Entrenamiento<br/>biomarcadores<br/>(GPU gratis)"]
        MODEL["modelo.pkl +<br/>métricas fairness"]
    end

    NAV["🌐 Navegador<br/>(Web Speech + Web Bluetooth)"]
    ESP["⌚ ESP32"]
    GEMINI["☁️ Gemini API"]

    NAV --> FE --> BE
    BE --> CH & SQ
    BE --> GEMINI
    NAV <-->|BLE| ESP
    TRAIN --> MODEL
    MODEL -.->|se copia a| BE
```
