# Diagramas de arquitectura — Nino (post-pivote)

Mermaid. Render en GitHub, VS Code (Markdown Preview Mermaid) o mermaid.live.

> **Alcance vigente (delimitación del hackathon):** recordatorios de una rutina cotidiana +
> **confirmación** + **aviso al cuidador** si no se cumple. Con **motor de criticidad** (lógica
> difusa) que respeta la autonomía. **NO** diagnostica, **NO** evalúa deterioro cognitivo, **NO**
> usa cámara. El monitoreo de vitales (smartwatch PPG) es **cardiovascular**, no cognitivo.
> Diagramas de la versión anterior (biomarcadores/cámara) → historial git y `backup/`.

---

## 1. C4 Nivel 1 — Contexto

```mermaid
graph TB
    subgraph Personas["Red de cuidado"]
        PAC["👵 Paciente<br/>(Alzheimer leve-moderado)"]
        CUI["🧑‍⚕️ Cuidador"]
        MED["👨‍⚕️ Médico"]
        FAM["👨‍👩‍👧 Familiar"]
        COM["🌐 Comunidad"]
    end

    SIS["🎼 NINO<br/>Asistente-guía de rutina orquestado por IA<br/>(RBAC · criticidad · offline-first)"]

    GEM["☁️ Gemini 2.5 Flash<br/>(solo online: conversación + reportes)"]
    SW["⌚ Smartwatch PPG<br/>(FC/HRV, presión estimada)"]
    LOC["📍 Ubicación<br/>(AirTag / GPS app)"]

    PAC -->|habla por voz| SIS
    SIS -->|recuerda, confirma, acompaña<br/>SIN forzar| PAC
    CUI -->|configura rutina + criticidad| SIS
    SIS -->|alerta SOLO si algo crítico falla| CUI
    MED -->|carga indicaciones/medicación| SIS
    SIS -->|adherencia + vitales (no cognitivo)| MED
    FAM -->|recibe sugerencias de contacto| SIS
    COM -->|matching de pares| SIS

    SIS <-->|online| GEM
    SW -->|vitales| SIS
    LOC -->|posición| SIS
```

---

## 2. C4 Nivel 2 — Contenedores

```mermaid
graph TB
    subgraph Front["FRONTEND (React + Vite)"]
        AP["📱 App Paciente<br/>/paciente · avatar Nino, solo voz"]
        AE["🖥️ App Equipo<br/>/ · dashboard por rol (RBAC)"]
    end

    subgraph Back["BACKEND (FastAPI :8001)"]
        ORQ["🎼 Orquestador (RBAC)<br/>5 agentes de rol"]
        CRIT["⭐ Motor de criticidad<br/>(lógica difusa)"]
        RUT["📅 Motor de rutina<br/>recordar→confirmar→escalar"]
        RAG["🔎 RAG (ChromaDB)<br/>twin paciente + jornada"]
        VIT["❤️ Vitales<br/>estimación presión PPG"]
        DB[("🗄️ SQLite<br/>Actividad · Alerta · Vital · Patient")]
    end

    GEM["☁️ Gemini 2.5 Flash"]
    EMB["🧠 Embeddings locales<br/>(sentence-transformers, offline)"]
    SW["⌚ Smartwatch ESP32 (PPG)"]

    AP -->|"POST /chat (voz)"| ORQ
    AE -->|"rutina, alertas, adherencia, vitales"| ORQ
    AE --> RUT
    ORQ --> RAG
    ORQ --> RUT
    RUT --> CRIT
    CRIT -->|escala lo crítico| DB
    RUT --> DB
    RAG --> EMB
    ORQ -.->|solo online| GEM
    SW -->|"POST /vitals"| VIT --> DB
    RAG --> DB
```

---

## 3. C4 Nivel 3 — Orquestador (RBAC) + criticidad

```mermaid
graph TB
    IN["Mensaje + rol autenticado"]
    ROUTER{"Role Router (RBAC)"}

    subgraph Agentes["Agentes por rol (scope + tools distintos)"]
        A1["Paciente<br/>consultar_pkg, rutina_hoy"]
        A2["Cuidador<br/>rutina_hoy, reporte_adherencia"]
        A3["Médico<br/>reporte_adherencia (NO cognitivo)"]
        A4["Familiar<br/>sugerir_contacto, consultar_pkg"]
        A5["Comunidad<br/>sugerir_contacto"]
    end

    GUARD["🛡️ Guardrails<br/>sin diagnóstico, sin evaluar deterioro"]
    MEM["🧠 Twin (RAG) + rutina"]

    IN --> ROUTER
    ROUTER --> A1 & A2 & A3 & A4 & A5
    A1 & A2 & A3 & A4 & A5 --> MEM
    A1 & A2 & A3 & A4 & A5 --> GUARD --> OUT["Respuesta trazable, cálida"]
```

---

## 4. ⭐ Motor de criticidad (el diferenciador)

```mermaid
flowchart TB
    subgraph IN["Entradas difusas"]
        C["criticidad de la actividad<br/>medicación/comida ~0.9 · hobby ~0.2"]
        R["retraso vs hora programada"]
        RC["receptividad del paciente<br/>(irritable ↔ receptivo)"]
        NR["nº de rechazos"]
    end

    FZ["Fuzzificación<br/>(membresías triangulares)"]
    RULES["Reglas Mamdani<br/>ej: crítico + muy tarde → escalar<br/>no-crítico + irritable → soltar"]
    DFZ["Defuzzificación<br/>(centroides) → insistencia [0-1]"]

    C & R & RC & NR --> FZ --> RULES --> DFZ --> ACC{"acción"}
    ACC -->|"0 – 0.25"| S["soltar<br/>(respeta autonomía)"]
    ACC -->|"0.25 – 0.5"| SU["sugerir suave"]
    ACC -->|"0.5 – 0.72"| F["recordar firme (cálido)"]
    ACC -->|"0.72 – 1"| E["🚨 escalar al cuidador"]

    S -.->|NUNCA fuerza| PAC["Paciente"]
    E -.->|enforcement = avisar,<br/>no coaccionar| CUI["Cuidador"]
```

---

## 5. Flujo de rutina — recordar → confirmar → escalar (secuencia)

```mermaid
sequenceDiagram
    autonumber
    participant R as 📅 Motor de rutina
    participant CR as ⭐ Criticidad
    participant N as 🤖 Nino (voz)
    participant P as 👵 Paciente
    participant AC as 🧑‍⚕️ Cuidador

    Note over R: Hora programada de una actividad
    R->>CR: evaluar(criticidad, retraso, receptividad)
    CR-->>R: acción + mensaje

    alt actividad NO crítica y paciente no quiere
        R->>N: soltar
        N->>P: "Está bien, lo dejamos para después" (no insiste)
    else actividad crítica (medicación/comida)
        R->>N: recordar firme
        N->>P: "¿Tomamos su pastilla juntos?"
        alt paciente confirma
            P->>N: "ya la tomé"
            N->>R: confirmar() → estado=confirmada
        else no se cumple / vencida
            R->>CR: reevaluar (retraso alto)
            CR-->>R: escalar_cuidador
            R->>AC: 🚨 Alerta "No tomó su medicación"
        end
    end
    Note over R,AC: Confirma y avisa SOLO lo crítico (no controla todo)
```

---

## 6. Vitales — smartwatch PPG (cardiovascular, no cognitivo)

```mermaid
flowchart LR
    SW["⌚ ESP32 + MAX30102"] -->|"FC + RR intervals"| HRV["calcula HRV (RMSSD)"]
    HRV -->|"WiFi POST /vitals"| BE["Backend"]
    BE --> EST["Estimación presión<br/>(PPG → sys/dia, NO diagnóstico)"]
    EST --> DB[("Vital")]
    DB --> DASH["Dashboard médico/cuidador"]
    SW -.->|botón| SOS["SOS + vibración"]
    Note["Justificación: ~81.6% de pacientes<br/>con demencia son hipertensos"]
```

---

## 7. Modos offline ↔ online (edge-first)

```mermaid
flowchart TB
    subgraph EDGE["EDGE / OFFLINE (siempre disponible)"]
        RUT2["Rutina + recordatorios"]
        CRIT2["Motor de criticidad"]
        CONF["Confirmación + alertas locales"]
        RAG2["Twin (ChromaDB + embeddings locales)"]
        TTS["Voz (Web Speech API navegador)"]
    end
    subgraph CLOUD["CLOUD / ONLINE (cuando hay red)"]
        LLM["Conversación rica (Gemini)"]
        REP["Reportes + metadata al equipo"]
        SYNC["Sync de eventos"]
    end
    EDGE -.->|si hay internet, sincroniza| CLOUD
    CLOUD -.->|si se cae la red, degrada a| EDGE
    Note2["Sin red: reminders, criticidad, confirmación,<br/>alertas y memoria funcionan igual.<br/>La nube solo AGREGA conversación y reportes."]
```

---

## 8. Despliegue (demo)

```mermaid
graph TB
    subgraph Laptop["💻 Laptop (demo)"]
        FE["Vite :5173<br/>/paciente + /"]
        BE["FastAPI :8001"]
        CH[("ChromaDB local")]
        SQ[("SQLite")]
    end
    NAV["🌐 Chrome/Edge<br/>Web Speech (voz)"]
    SW["⌚ ESP32 smartwatch<br/>WiFi → /vitals"]
    GEM["☁️ Gemini API"]

    NAV --> FE -->|VITE_API_URL| BE
    BE --> CH & SQ
    BE -.->|online| GEM
    SW -->|POST /vitals| BE
```
