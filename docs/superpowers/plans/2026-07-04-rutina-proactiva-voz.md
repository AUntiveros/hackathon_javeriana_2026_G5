# Rutina Proactiva + Confirmación por Voz Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hacer que Tito (app paciente) avise proactivamente por horario, valide la toma de pastillas por voz, responda con detalle sobre medicación/actividad física, muestre alertas reales al cuidador, y quitar el rol Comunidad del producto.

**Architecture:** Todo el mecanismo de avisos/confirmación vive en el cliente (`useAcompanante.ts`), reutilizando endpoints y el motor de criticidad que YA existen en el backend (`/routine`, `/actividades/*`, `/alertas/*`). El único cambio de backend es de contenido (seed + prompt) y una pequeña ampliación de `_act_dict()` para exponer campos que ya existen en el modelo. No se toca `backend/criticality/engine.py` ni se crea `backend/risk/*` (motor de riesgo bayesiano: track paralelo ya en curso, ver `docs/superpowers/specs/2026-07-04-motor-riesgo-bayesiano-design.md`).

**Tech Stack:** FastAPI + SQLModel (backend), React + TypeScript + Vite (frontend), Web Speech API (STT/TTS), conda env `medtrack-engine`.

## Global Constraints

- No modificar `backend/criticality/engine.py` ni crear archivos bajo `backend/risk/`.
- No tocar `TwinDashboard`/`WearablePanel` dentro de `CuidadorView` en este plan.
- El paciente en el seed es "Don Manuel" (ya migrado) — todo texto nuevo debe usar ese nombre, nunca "Don José".
- El asistente se llama "Tito" (ya migrado) — ningún texto nuevo debe decir "Nino".
- Sin emojis en la app del paciente (`PacienteApp.tsx`, `Tito.tsx`, `useAcompanante.ts`) — ya se limpiaron, no reintroducir.
- `tsc --noEmit` debe quedar limpio en `frontend/` al final de cada tarea de frontend.

---

### Task 1: Eliminar el rol Comunidad

**Files:**
- Modify: `backend/orchestrator/agents.py:47-53` (borrar entrada `"comunidad"` del dict `ROLES`)
- Modify: `frontend/src/api/types.ts:9` (quitar `'comunidad'` del type `Rol`)
- Modify: `frontend/src/components/RoleSelector.tsx:9` (quitar chip)
- Modify: `frontend/src/apps/EquipoApp.tsx` (quitar import, subtítulo, render condicional)
- Modify: `frontend/src/api/mock.ts` (quitar entrada `comunidad` de `RESPUESTAS_POR_ROL` y de `turnos`)
- Delete: `frontend/src/views/ComunidadView.tsx`
- Delete: `frontend/src/views/comunidad.css`

**Interfaces:**
- Produces: `Rol` type sin `'comunidad'` (usado por todas las tareas siguientes que tocan frontend).

- [ ] **Step 1: Quitar el rol del backend**

En `backend/orchestrator/agents.py`, borrar el bloque completo:

```python
    "comunidad": RolConfig(
        "comunidad",
        "Conectas al paciente con pares de intereses comunes para combatir el aislamiento. Tono "
        "social e inclusivo. No expongas datos sensibles.",
        tools=["sugerir_contacto"],
        scope=["intereses"],
    ),
```

- [ ] **Step 2: Verificar que el backend rechaza el rol**

Con el backend corriendo (`uvicorn backend.main:app --port 8000`, env `medtrack-engine`):

```bash
curl -s -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" \
  -d '{"rol":"comunidad","mensaje":"hola","patient_id":1}'
```

Expected: `{"error":"rol desconocido: comunidad","roles_validos":["paciente","cuidador","medico","familiar"]}`

- [ ] **Step 3: Quitar el rol del tipo compartido**

En `frontend/src/api/types.ts:9`:

```ts
export type Rol = 'paciente' | 'cuidador' | 'medico' | 'familiar';
```

- [ ] **Step 4: Quitar el chip del selector**

En `frontend/src/components/RoleSelector.tsx`, la constante `ROLES` queda:

```ts
const ROLES: { id: Rol; label: string; icono: string }[] = [
  { id: 'paciente', label: 'Paciente', icono: '🧓' },
  { id: 'cuidador', label: 'Cuidador', icono: '🤝' },
  { id: 'medico', label: 'Médico', icono: '🩺' },
  { id: 'familiar', label: 'Familiar', icono: '👨‍👩‍👧' },
];
```

- [ ] **Step 5: Quitar la vista del router de EquipoApp**

En `frontend/src/apps/EquipoApp.tsx`, borrar la línea `import ComunidadView from '../views/ComunidadView';`, la entrada `comunidad: 'Red de pares — club de adulto mayor',` de `SUBTITULO`, y la línea `{rol === 'comunidad' && <ComunidadView />}`. El archivo completo queda:

```tsx
import { useState } from 'react';
import RoleSelector from '../components/RoleSelector';
import CuidadorView from '../views/CuidadorView';
import MedicoView from '../views/MedicoView';
import FamiliarView from '../views/FamiliarView';
import type { Rol } from '../api/types';

const SUBTITULO: Partial<Record<Rol, string>> = {
  cuidador: 'Cuidador aumentado — Don Manuel',
  medico: 'Señales clínicas del habla — Don Manuel',
  familiar: 'Cómo está tu papá hoy',
};

/**
 * App del Equipo de cuidado: cuidador, médico, familiar.
 * La experiencia del paciente vive aparte en /paciente (cero menús).
 */
export default function EquipoApp() {
  const [rol, setRol] = useState<Rol>('cuidador');

  return (
    <main className="app">
      <header className="app__header">
        <h1>Tito · Equipo</h1>
        <p>{SUBTITULO[rol]}</p>
      </header>

      <RoleSelector rol={rol} onCambio={setRol} excluir={['paciente']} />

      {rol === 'cuidador' && <CuidadorView />}
      {rol === 'medico' && <MedicoView />}
      {rol === 'familiar' && <FamiliarView />}

      <a className="app__link-paciente" href="/paciente">
        Ver la app del paciente →
      </a>
    </main>
  );
}
```

- [ ] **Step 6: Borrar la vista y su CSS**

```bash
git rm frontend/src/views/ComunidadView.tsx frontend/src/views/comunidad.css
```

- [ ] **Step 7: Limpiar el mock**

En `frontend/src/api/mock.ts`, borrar del objeto `RESPUESTAS_POR_ROL` (líneas ~75-82) la entrada:

```ts
  comunidad: [
    {
      respuesta:
        'Hay 2 vecinos del club de adulto mayor con intereses parecidos a los de Don Manuel: don Ernesto (también ex-agricultor) y doña Carmen (fan de la música criolla). ¿Coordino un encuentro para el sábado?',
      emocion: 'feliz',
      tools_usadas: ['matching_pares'],
    },
  ],
```

Y en el objeto `turnos` (línea ~90), borrar la línea `comunidad: 0,`.

- [ ] **Step 8: Typecheck**

```bash
cd frontend && npx tsc --noEmit
```

Expected: sin salida (sin errores).

- [ ] **Step 9: Commit**

```bash
git add backend/orchestrator/agents.py frontend/src/api/types.ts frontend/src/api/mock.ts \
  frontend/src/components/RoleSelector.tsx frontend/src/apps/EquipoApp.tsx
git commit -m "Eliminar rol Comunidad del backend y frontend"
```

---

### Task 2: Enriquecer datos de rutina (condición, dosis/día, beneficio)

**Files:**
- Modify: `backend/db/seed.py:45-52` (lista `rutina`)
- Modify: `backend/routine/engine.py:43-46` (`_act_dict`)
- Delete + regenerate: `backend/app.db`

**Interfaces:**
- Produces: cada actividad de tipo `medicacion`/`actividad` trae ahora `detalle: dict` y `ventana_min: int` en la respuesta de `/routine/{pid}/today` y en el contexto `rutina_hoy` que reciben los agentes — usado por Task 3 (prompt) y Task 4 (polling en frontend).

- [ ] **Step 1: Ampliar la rutina sembrada**

En `backend/db/seed.py`, reemplazar la lista `rutina` (dentro de `seed()`) — quitar la única fila de "Pastilla de la presión" y agregar 3 tomas con `detalle`, y agregar `detalle` a la caminata. Como `Actividad.detalle` es un campo del modelo (no del tuple actual), hay que cambiar el tuple por un dict por actividad. Reemplazar:

```python
        rutina = [
            ("Pastilla de la memoria (donepezilo)", "medicacion", 0.9, "08:30", 30),
            ("Aseo de la mañana", "autocuidado", 0.6, "09:00", 90),
            ("Almuerzo", "comida", 0.85, "13:00", 60),
            ("Leer el libro de la semana", "hobby", 0.2, "16:00", 180),
            ("Caminata de la tarde", "actividad", 0.35, "17:00", 120),
            ("Pastilla de la presión", "medicacion", 0.9, "20:00", 30),
        ]
        for nombre, tipo, crit, hora, ventana in rutina:
            s.add(Actividad(patient_id=1, nombre=nombre, tipo=tipo, criticidad_base=crit,
                            hora=hora, ventana_min=ventana, fecha=hoy))
```

por:

```python
        rutina = [
            ("Pastilla de la memoria (donepezilo)", "medicacion", 0.9, "08:30", 30, {}),
            ("Aseo de la mañana", "autocuidado", 0.6, "09:00", 90, {}),
            ("Almuerzo", "comida", 0.85, "13:00", 60, {}),
            ("Leer el libro de la semana", "hobby", 0.2, "16:00", 180, {}),
            ("Caminata de la tarde", "actividad", 0.35, "17:00", 120,
             {"beneficio": "hipertensión", "pasos_meta": 1500}),
            ("Pastilla de la presión", "medicacion", 0.9, "08:00", 30,
             {"condicion": "hipertensión", "dosis_dia": 3}),
            ("Pastilla de la presión", "medicacion", 0.9, "14:00", 30,
             {"condicion": "hipertensión", "dosis_dia": 3}),
            ("Pastilla de la presión", "medicacion", 0.9, "20:00", 30,
             {"condicion": "hipertensión", "dosis_dia": 3}),
        ]
        for nombre, tipo, crit, hora, ventana, detalle in rutina:
            s.add(Actividad(patient_id=1, nombre=nombre, tipo=tipo, criticidad_base=crit,
                            hora=hora, ventana_min=ventana, fecha=hoy, detalle=detalle))
```

- [ ] **Step 2: Exponer `detalle` y `ventana_min` en la API de rutina**

En `backend/routine/engine.py`, reemplazar:

```python
def _act_dict(a: Actividad) -> dict:
    return {"id": a.id, "nombre": a.nombre, "tipo": a.tipo, "hora": a.hora,
            "criticidad": a.criticidad_base, "estado": a.estado,
            "n_recordatorios": a.n_recordatorios, "n_rechazos": a.n_rechazos}
```

por:

```python
def _act_dict(a: Actividad) -> dict:
    return {"id": a.id, "nombre": a.nombre, "tipo": a.tipo, "hora": a.hora,
            "criticidad": a.criticidad_base, "estado": a.estado,
            "n_recordatorios": a.n_recordatorios, "n_rechazos": a.n_rechazos,
            "ventana_min": a.ventana_min, "detalle": a.detalle}
```

- [ ] **Step 3: Regenerar la base de datos de demo**

`backend/db/seed.py` no sobreescribe si el paciente ya existe, así que hay que partir de cero (dato de demo, sin pérdida real — confirmar que no hay nada que el usuario quiera conservar antes de borrar):

```bash
cd "D:\UNIDAD D\UNIVERSIDAD\2026-1\Hackathon Javeriana"
rm backend/app.db
"/c/Users/Alvaro/anaconda3/envs/medtrack-engine/python.exe" -m backend.db.seed
```

Expected: `[seed] paciente + rutina del día cargados`

- [ ] **Step 4: Verificar el contenido servido**

```bash
"/c/Users/Alvaro/anaconda3/envs/medtrack-engine/python.exe" -m uvicorn backend.main:app --port 8000 &
sleep 2
curl -s http://127.0.0.1:8000/routine/1/today
```

Expected: JSON con 8 actividades, 3 de ellas `"nombre":"Pastilla de la presión"` en horas `08:00`/`14:00`/`20:00`, cada una con `"detalle":{"condicion":"hipertensión","dosis_dia":3}` y `"ventana_min":30`; la caminata con `"detalle":{"beneficio":"hipertensión","pasos_meta":1500}`.

- [ ] **Step 5: Commit**

```bash
git add backend/db/seed.py backend/routine/engine.py
git commit -m "Enriquecer rutina con condicion/dosis por actividad (pastilla presion 3x/dia)"
```

---

### Task 3: Ampliar el system prompt del rol paciente

**Files:**
- Modify: `backend/orchestrator/agents.py:22-30` (`ROLES["paciente"]`)

**Interfaces:**
- Consumes: `detalle`/`ventana_min` producidos en Task 2, ya presentes en el contexto `rutina_hoy` que el router arma para este rol (`router.py` ya inyecta `tools.rutina_hoy(patient_id)` como texto en el prompt).

- [ ] **Step 1: Reescribir el prompt**

En `backend/orchestrator/agents.py`, reemplazar la entrada `"paciente"` de `ROLES`:

```python
    "paciente": RolConfig(
        "paciente",
        "Eres el compañero de IA de un adulto mayor con Alzheimer leve. Habla cálido, sencillo, "
        "frases cortas, de 'usted'. Usa su memoria (contexto) para recordarle personas y hechos "
        "con cariño y fomentar que hable de sus recuerdos (reminiscencia). NUNCA lo alarmes ni "
        "des diagnósticos. Si no sabes algo, no lo inventes.",
        tools=["consultar_pkg", "rutina_hoy"],
        scope=["pkg", "rutina"],
    ),
```

por:

```python
    "paciente": RolConfig(
        "paciente",
        "Eres el compañero de IA de un adulto mayor con Alzheimer leve. Habla cálido, sencillo, "
        "frases cortas, de 'usted'. Usa su memoria (contexto) para recordarle personas y hechos "
        "con cariño y fomentar que hable de sus recuerdos (reminiscencia). NUNCA lo alarmes ni "
        "des diagnósticos. Si no sabes algo, no lo inventes.\n\n"
        "Cuando pregunte por sus pastillas o su rutina, usa el bloque 'Rutina de hoy y su estado': "
        "cada actividad trae un campo 'detalle' con la condición que trata (ej. hipertensión) y "
        "'dosis_dia' si es una pastilla de varias tomas al día. Cuenta cuántas de esa pastilla ya "
        "están en estado 'confirmada' hoy frente al total, y dígale la hora de la siguiente que "
        "siga 'pendiente'. Si el paciente dice que está aburrido, sin ganas, o no sabe qué hacer, "
        "sugiérale con cariño la actividad física pendiente de hoy, mencionando el beneficio de su "
        "'detalle' (ej. caminar ayuda a controlar la presión).",
        tools=["consultar_pkg", "rutina_hoy"],
        scope=["pkg", "rutina"],
    ),
```

- [ ] **Step 2: Verificar con el backend corriendo (reload activo o reiniciar)**

```bash
printf '{"rol":"paciente","mensaje":"que pastillas tengo pendientes hoy","patient_id":1}' > /tmp/t3.json
curl -s -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" --data-binary @/tmp/t3.json
```

Expected: la respuesta menciona la presión/hipertensión, que son 3 veces al día, y una hora concreta de la siguiente toma pendiente (comparar con la hora actual y las 3 filas sembradas en Task 2).

```bash
printf '{"rol":"paciente","mensaje":"no se que hacer","patient_id":1}' > /tmp/t3b.json
curl -s -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" --data-binary @/tmp/t3b.json
```

Expected: la respuesta sugiere la caminata de la tarde y menciona el beneficio para la presión.

- [ ] **Step 3: Commit**

```bash
git add backend/orchestrator/agents.py
git commit -m "Ampliar prompt del paciente para detalle de medicacion y sugerencia de actividad fisica"
```

---

### Task 4: Tipos de frontend + polling proactivo + aviso puntual por horario

**Files:**
- Modify: `frontend/src/api/types.ts:106-125` (`ActividadV2`, `DecisionCriticidad`)
- Modify: `frontend/src/hooks/useAcompanante.ts`

**Interfaces:**
- Consumes: `getActividadesHoy(patientId): Promise<{actividades: ActividadV2[]}>`, `procesarRutina(patientId, receptividad?): Promise<{recordatorios: DecisionCriticidad[]}>` (ya existen en `frontend/src/api/client.ts:95-101`).
- Produces: `esperandoConfirmacionRef.current: number | null` (id de actividad de medicación pendiente de confirmar) y `cooldownRef.current: Map<number, number>` (timestamp ms hasta el que no re-avisar esa actividad) — consumidos por Task 5 en el mismo archivo.

- [ ] **Step 1: Ampliar los tipos**

En `frontend/src/api/types.ts`, reemplazar:

```ts
export interface ActividadV2 {
  id: number;
  nombre: string;
  tipo: 'medicacion' | 'comida' | 'cita' | 'autocuidado' | 'hobby' | 'actividad';
  hora: string;            // "08:30"
  criticidad: number;      // 0-1
  estado: 'pendiente' | 'confirmada' | 'omitida' | 'reprogramada';
  n_recordatorios: number;
  n_rechazos: number;
}
```

por:

```ts
export interface ActividadV2 {
  id: number;
  nombre: string;
  tipo: 'medicacion' | 'comida' | 'cita' | 'autocuidado' | 'hobby' | 'actividad';
  hora: string;            // "08:30"
  criticidad: number;      // 0-1
  estado: 'pendiente' | 'confirmada' | 'omitida' | 'reprogramada';
  n_recordatorios: number;
  n_rechazos: number;
  ventana_min: number;
  detalle: Record<string, unknown>;
}
```

Y reemplazar:

```ts
export interface DecisionCriticidad {
  accion: 'soltar' | 'sugerir_suave' | 'recordar_firme' | 'escalar_cuidador';
  insistencia: number;
  alertar_cuidador: boolean;
  tono: string;
  mensaje?: string;
  retraso_min?: number;
}
```

por:

```ts
export interface DecisionCriticidad {
  actividad_id?: number;
  nombre?: string;
  accion: 'soltar' | 'sugerir_suave' | 'recordar_firme' | 'escalar_cuidador';
  insistencia: number;
  alertar_cuidador: boolean;
  tono: string;
  mensaje?: string;
  retraso_min?: number;
}
```

- [ ] **Step 2: Typecheck de solo-tipos**

```bash
cd frontend && npx tsc --noEmit
```

Expected: sin errores (los campos nuevos son opcionales o se agregan a un tipo no usado aún con valores literales incompletos en otro lado; si algo se queja, es porque algún mock construye un `ActividadV2` a mano sin `ventana_min`/`detalle` — no debería ser el caso, `mock.ts` no usa `ActividadV2`).

- [ ] **Step 3: Importar lo necesario en el hook**

En `frontend/src/hooks/useAcompanante.ts:1-2`, reemplazar:

```ts
import { useCallback, useEffect, useRef, useState } from 'react';
import { chat, PATIENT_ID } from '../api/client';
```

por:

```ts
import { useCallback, useEffect, useRef, useState } from 'react';
import { chat, confirmarActividad, getActividadesHoy, procesarRutina, rechazarActividad, PATIENT_ID } from '../api/client';
import type { ActividadV2 } from '../api/types';
```

(`confirmarActividad`/`rechazarActividad` se usan recién en Task 5, pero se importan juntos para no volver a tocar esta línea.)

- [ ] **Step 4: Agregar refs de seguimiento**

En `frontend/src/hooks/useAcompanante.ts`, dentro de `useAcompanante()`, justo debajo de la línea `const vivoRef = useRef(false);` (línea 56), agregar:

```ts
  const avisadasHoyRef = useRef<Set<number>>(new Set());
  const avisadasFechaRef = useRef('');
  const cooldownRef = useRef<Map<number, number>>(new Map());
  const esperandoConfirmacionRef = useRef<number | null>(null);
```

- [ ] **Step 5: Agregar helpers de horario y mensaje fuera del hook**

En `frontend/src/hooks/useAcompanante.ts`, antes de la función `detenerRec` al final del archivo (línea 282), agregar:

```ts
function dentroDeVentana(hora: string, ventanaMin: number): boolean {
  const [h, m] = hora.split(':').map(Number);
  const ahora = new Date();
  const programada = new Date(ahora);
  programada.setHours(h, m, 0, 0);
  const transcurridoMin = (ahora.getTime() - programada.getTime()) / 60_000;
  return transcurridoMin >= 0 && transcurridoMin <= ventanaMin;
}

function mensajeHoraLlegada(a: ActividadV2): string {
  const n = a.nombre.toLowerCase();
  if (a.tipo === 'medicacion') return `Don Manuel, es hora de su ${n}. ¿La tomamos juntos ahora?`;
  if (a.tipo === 'comida') return `Ya es hora de ${n}. ¿Comemos algo rico?`;
  return `Le recuerdo con cariño: es hora de «${a.nombre}».`;
}

const RE_NO = /\b(no s[eé]|todav[ií]a no|a[uú]n no|no)\b/i;
const RE_SI = /\b(s[ií]|ya|list[oa]|tomad[oa]|me la tom[eé])\b/i;

function detectarConfirmacion(texto: string): 'si' | 'no' | null {
  if (RE_NO.test(texto)) return 'no';
  if (RE_SI.test(texto)) return 'si';
  return null;
}
```

- [ ] **Step 6: Agregar `anunciar` y `revisarRutina`**

En `frontend/src/hooks/useAcompanante.ts`, justo después del cierre de `armarTimerSilencio` (después de la línea `}, [setEstadoTotal]);` que sigue a la sección `// ---------- silencio → volver a dormir ----------`, agregar:

```ts
  // ---------- avisos proactivos por horario ----------

  const anunciar = useCallback(
    (mensaje: string) => {
      setEstadoTotal('hablando');
      setFrase(mensaje);
      setEmocion('neutral');
      hablar(mensaje, () => {
        if (!vivoRef.current) return;
        setEstadoTotal('atento');
        setFrase('Lo escucho…');
        armarTimerSilencio();
        arrancarRec();
      });
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [hablar, armarTimerSilencio],
  );

  const revisarRutina = useCallback(async () => {
    if (!vivoRef.current) return;
    if (estadoRef.current === 'hablando' || estadoRef.current === 'pensando') return;

    const hoy = new Date().toISOString().slice(0, 10);
    if (avisadasFechaRef.current !== hoy) {
      avisadasFechaRef.current = hoy;
      avisadasHoyRef.current.clear();
      cooldownRef.current.clear();
    }

    const { actividades } = await getActividadesHoy(PATIENT_ID);
    const reciénLlegada = actividades.find(
      (a) =>
        a.estado === 'pendiente' &&
        !avisadasHoyRef.current.has(a.id) &&
        dentroDeVentana(a.hora, a.ventana_min),
    );
    if (reciénLlegada) {
      avisadasHoyRef.current.add(reciénLlegada.id);
      if (reciénLlegada.tipo === 'medicacion') esperandoConfirmacionRef.current = reciénLlegada.id;
      anunciar(mensajeHoraLlegada(reciénLlegada));
      return; // un aviso por ciclo: no saturar al paciente
    }

    const ahora = Date.now();
    const { recordatorios } = await procesarRutina(PATIENT_ID);
    const urgente = recordatorios.find(
      (r) =>
        r.accion !== 'soltar' &&
        r.mensaje &&
        r.actividad_id !== undefined &&
        (cooldownRef.current.get(r.actividad_id) ?? 0) <= ahora,
    );
    if (urgente?.mensaje && urgente.actividad_id !== undefined) {
      cooldownRef.current.set(urgente.actividad_id, ahora + 15 * 60_000);
      if (urgente.nombre?.toLowerCase().includes('pastilla')) {
        esperandoConfirmacionRef.current = urgente.actividad_id;
      }
      anunciar(urgente.mensaje);
    }
  }, [anunciar]);

  useEffect(() => {
    const id = window.setInterval(() => {
      void revisarRutina();
    }, 90_000);
    return () => window.clearInterval(id);
  }, [revisarRutina]);
```

- [ ] **Step 7: Typecheck**

```bash
cd frontend && npx tsc --noEmit
```

Expected: sin errores.

- [ ] **Step 8: Verificación manual del aviso puntual**

Con backend y frontend corriendo (`npm run dev` en `frontend/`, `VITE_API_URL=http://localhost:8000`), crear una actividad de prueba que caiga dentro de la ventana ahora mismo:

```bash
AHORA=$(date +%H:%M)
printf '{"patient_id":1,"nombre":"Prueba de aviso","tipo":"actividad","criticidad_base":0.5,"hora":"%s","ventana_min":5}' "$AHORA" > /tmp/prueba.json
curl -s -X POST http://127.0.0.1:8000/actividades -H "Content-Type: application/json" --data-binary @/tmp/prueba.json
```

Abrir `/paciente` en el navegador, tocar "Encender a Tito", esperar hasta 90s. Expected: Tito dice en voz alta "Le recuerdo con cariño: es hora de «Prueba de aviso»." sin que se le pregunte nada.

- [ ] **Step 9: Commit**

```bash
git add frontend/src/api/types.ts frontend/src/hooks/useAcompanante.ts
git commit -m "Agregar polling proactivo y aviso puntual por horario en useAcompanante"
```

---

### Task 5: Confirmación de pastilla por voz

**Files:**
- Modify: `frontend/src/hooks/useAcompanante.ts` (dentro de `arrancarRec`, handler `rec.onresult`)

**Interfaces:**
- Consumes: `esperandoConfirmacionRef`, `cooldownRef`, `detectarConfirmacion`, `anunciar` (Task 4, mismo archivo); `confirmarActividad(id)`, `rechazarActividad(id)` (ya en `client.ts:107-113`).

- [ ] **Step 1: Interceptar la respuesta cuando se espera confirmación**

En `frontend/src/hooks/useAcompanante.ts`, dentro de `arrancarRec`, el handler `rec.onresult` tiene esta rama:

```ts
      } else if (est === 'atento') {
        void conversar(texto);
      }
```

Reemplazar por:

```ts
      } else if (est === 'atento') {
        const actId = esperandoConfirmacionRef.current;
        if (actId !== null) {
          const decision = detectarConfirmacion(texto);
          if (decision === 'si') {
            esperandoConfirmacionRef.current = null;
            void confirmarActividad(actId);
            anunciar('¡Qué bien! Anotado, gracias por avisarme.');
            return;
          }
          if (decision === 'no') {
            esperandoConfirmacionRef.current = null;
            void rechazarActividad(actId);
            cooldownRef.current.set(actId, Date.now() + 15 * 60_000);
            anunciar('Está bien, no se preocupe. Se lo recuerdo en un ratito.');
            return;
          }
          esperandoConfirmacionRef.current = null; // no coincide: sigue como conversación normal
        }
        void conversar(texto);
      }
```

- [ ] **Step 2: Typecheck**

```bash
cd frontend && npx tsc --noEmit
```

Expected: sin errores. (`anunciar` está declarado antes de `arrancarRec` en el archivo — confirmar que el orden de declaración en Task 4 Step 6 quedó antes de la sección `// ---------- reconocimiento continuo ----------`; si no, moverlo antes de usarlo, ya que son `useCallback` y JS no hace hoisting de `const`.)

- [ ] **Step 3: Verificación manual del flujo completo**

Con la actividad de prueba de Task 4 Step 8 ya confirmada/limpia, repetir con una de tipo `medicacion`:

```bash
AHORA=$(date +%H:%M)
printf '{"patient_id":1,"nombre":"Pastilla de prueba","tipo":"medicacion","criticidad_base":0.9,"hora":"%s","ventana_min":5}' "$AHORA" > /tmp/pastilla.json
curl -s -X POST http://127.0.0.1:8000/actividades -H "Content-Type: application/json" --data-binary @/tmp/pastilla.json
```

Abrir `/paciente`, encender a Tito, esperar el aviso ("¿La tomamos juntos ahora?"). Responder por voz (o texto si no hay STT) "no todavía". Expected: Tito responde "Está bien, no se preocupe...", y:

```bash
curl -s http://127.0.0.1:8000/routine/1/today | grep -o '"nombre":"Pastilla de prueba"[^}]*"n_rechazos":[0-9]*'
```

muestra `n_rechazos` en 1. Repetir la prueba respondiendo "sí" en otra actividad de prueba nueva y confirmar que su `estado` pasa a `"confirmada"`.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/hooks/useAcompanante.ts
git commit -m "Agregar confirmacion de pastilla por voz con matcher si/no y cooldown"
```

---

### Task 6: Vista Cuidador con alertas reales

**Files:**
- Modify: `frontend/src/views/CuidadorView.tsx`
- Modify: `frontend/src/views/cuidador.css`

**Interfaces:**
- Consumes: `getActividadesHoy`, `confirmarActividad`, `getAlertas`, `atenderAlerta`, `PATIENT_ID` (`client.ts`); `ActividadV2`, `AlertaCuidador` (`types.ts`).

- [ ] **Step 1: Reescribir la vista**

Reemplazar todo el contenido de `frontend/src/views/CuidadorView.tsx` por:

```tsx
import { useEffect, useState } from 'react';
import TwinDashboard from '../components/TwinDashboard/TwinDashboard';
import WearablePanel from '../components/WearablePanel/WearablePanel';
import { atenderAlerta, confirmarActividad, getActividadesHoy, getAlertas, PATIENT_ID } from '../api/client';
import type { ActividadV2, AlertaCuidador } from '../api/types';
import './cuidador.css';

const ICONO: Record<ActividadV2['tipo'], string> = {
  medicacion: '💊',
  comida: '🍽️',
  cita: '🏥',
  autocuidado: '🧼',
  hobby: '🎨',
  actividad: '🚶',
};

/**
 * Vista Cuidador: agenda del día (motor de rutina v2) + alertas del motor de criticidad.
 */
export default function CuidadorView() {
  const [agenda, setAgenda] = useState<ActividadV2[]>([]);
  const [alertas, setAlertas] = useState<AlertaCuidador[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    void Promise.all([getActividadesHoy(PATIENT_ID), getAlertas(PATIENT_ID)]).then(([act, al]) => {
      setAgenda(act.actividades);
      setAlertas(al);
      setCargando(false);
    });
    const id = window.setInterval(() => {
      void getAlertas(PATIENT_ID).then(setAlertas);
    }, 60_000);
    return () => window.clearInterval(id);
  }, []);

  const marcarHecho = async (id: number) => {
    setAgenda((prev) => prev.map((a) => (a.id === id ? { ...a, estado: 'confirmada' } : a)));
    await confirmarActividad(id);
  };

  const marcarAtendida = async (id: number) => {
    setAlertas((prev) => prev.map((a) => (a.id === id ? { ...a, atendida: true } : a)));
    await atenderAlerta(id);
  };

  const pendientes = alertas.filter((a) => !a.atendida);

  return (
    <div className="vista">
      {pendientes.length > 0 && (
        <section className="tarjeta alertas">
          <h2>Alertas</h2>
          <ul className="alertas__lista">
            {pendientes.map((a) => (
              <li key={a.id} className={`alertas__item alertas__item--${a.nivel}`}>
                <span className="alertas__motivo">{a.motivo}</span>
                <button className="alertas__boton" onClick={() => void marcarAtendida(a.id)}>
                  Atender
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="tarjeta">
        <h2>Agenda de hoy — Don Manuel</h2>
        {cargando && <p className="cargando">Cargando agenda…</p>}
        <ul className="agenda">
          {agenda.map((a) => (
            <li
              key={a.id}
              className={`agenda__item agenda__item--${a.estado === 'confirmada' ? 'hecho' : 'pendiente'}`}
            >
              <span className="agenda__hora">{a.hora}</span>
              <span className="agenda__icono" aria-hidden="true">{ICONO[a.tipo]}</span>
              <span className="agenda__cuerpo">
                <strong>{a.nombre}</strong>
                <small>{a.tipo} · criticidad {(a.criticidad * 100).toFixed(0)}%</small>
              </span>
              {a.estado === 'confirmada' ? (
                <span className="agenda__hecho" aria-label="hecho">✓</span>
              ) : (
                <button className="agenda__boton" onClick={() => void marcarHecho(a.id)}>
                  Hecho
                </button>
              )}
            </li>
          ))}
        </ul>
      </section>

      <section className="tarjeta consejo">
        <h2>Consejo de hoy</h2>
        <p>
          Evita preguntarle <em>"¿te acuerdas?"</em>. Mejor cuéntale tú la anécdota y deja que él
          la complete — reduce frustración y estimula memoria episódica.
        </p>
      </section>

      <WearablePanel />

      <TwinDashboard variante="resumen" />
    </div>
  );
}
```

- [ ] **Step 2: Agregar estilos de alertas**

Al final de `frontend/src/views/cuidador.css`, agregar:

```css
.alertas__lista {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.alertas__item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.6rem;
  padding: 0.6rem 0.8rem;
  border-radius: 12px;
  border-left: 6px solid #C9B8A8;
  background: #FFF6EC;
}

.alertas__item--alto {
  border-left-color: #d03b3b;
}

.alertas__item--medio {
  border-left-color: #E76F51;
}

.alertas__item--bajo {
  border-left-color: #8A7468;
}

.alertas__motivo {
  font-size: 0.98rem;
  color: #3E322C;
}

.alertas__boton {
  min-height: 40px;
  padding: 0 0.9rem;
  border: none;
  border-radius: 999px;
  background: #5C4B44;
  color: #FFF8F0;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
}
```

- [ ] **Step 3: Typecheck**

```bash
cd frontend && npx tsc --noEmit
```

Expected: sin errores.

- [ ] **Step 4: Verificación manual de alertas**

Forzar una escalada real: rechazar la misma actividad de prueba 2 veces seguidas y luego procesar pendientes.

```bash
curl -s -X POST http://127.0.0.1:8000/actividades/<ID>/rechazar
curl -s -X POST http://127.0.0.1:8000/actividades/<ID>/rechazar
curl -s -X POST http://127.0.0.1:8000/routine/1/procesar -H "Content-Type: application/json" -d '{"receptividad":0.3}'
curl -s http://127.0.0.1:8000/alertas/1
```

Expected: `/alertas/1` devuelve al menos una alerta con `"atendida":false`. Abrir `/` (EquipoApp) → Cuidador → debe verse la sección "Alertas" con esa entrada y el botón "Atender" funcionando (al click, desaparece de la lista tras `atenderAlerta`).

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/CuidadorView.tsx frontend/src/views/cuidador.css
git commit -m "Migrar CuidadorView a endpoints v2 y mostrar alertas reales"
```

---

### Task 7: Verificación end-to-end completa

**Files:** ninguno (solo verificación)

- [ ] **Step 1: Arranque limpio del backend**

```bash
cd "D:\UNIDAD D\UNIVERSIDAD\2026-1\Hackathon Javeriana"
netstat -ano | grep ":8000" | grep LISTENING   # confirmar que no hay nada corriendo; si hay, matarlo
"/c/Users/Alvaro/anaconda3/envs/medtrack-engine/python.exe" -m uvicorn backend.main:app --reload --port 8000
```

- [ ] **Step 2: Arranque del frontend**

```bash
cd frontend
cat .env   # confirmar VITE_API_URL=http://localhost:8000
npm run dev
```

- [ ] **Step 3: Checklist funcional**

- [ ] `GET /routine/1/today` trae 8 actividades, 3 pastillas de presión con `detalle.condicion="hipertensión"`.
- [ ] Rol Comunidad no aparece en `RoleSelector` ni responde en `/chat`.
- [ ] Preguntar a Tito "¿qué pastillas tengo pendientes hoy?" → menciona hipertensión, 3 veces al día, cuántas lleva, hora de la siguiente.
- [ ] Decir "no sé qué hacer" → sugiere la caminata y su beneficio.
- [ ] Con una actividad de prueba dentro de su ventana horaria y la app abierta → Tito avisa solo, sin que se le pregunte, dentro de 90s.
- [ ] Tras un aviso de medicación, responder "no" → confirma rechazo (`n_rechazos` sube), no queda marcada como tomada, se reprograma para ~15 min.
- [ ] Responder "sí" a otro aviso de medicación → la actividad pasa a `estado: "confirmada"`.
- [ ] Tras 2 rechazos seguidos + `POST /routine/1/procesar` → aparece una `Alerta` nueva, visible en Cuidador con botón "Atender" funcional.
- [ ] `cd frontend && npx tsc --noEmit` sin errores.

- [ ] **Step 4: Cierre**

Dejar el backend corriendo en `:8000` y el frontend en su puerto de Vite (mostrado en la consola de `npm run dev`) listos para la demo de mañana.
