# Motor de riesgo global (Fuzzy-Bayesian Network) — Diseño

## Contexto y problema

El motor de criticidad actual (`backend/criticality/engine.py`) es un sistema difuso Mamdani puro-Python que evalúa **una actividad a la vez**: dado (criticidad, retraso, receptividad, n_rechazos) decide cuánto insistir (soltar/sugerir_suave/recordar_firme/escalar_cuidador). Funciona bien y está probado, pero no combina múltiples señales simultáneas del paciente en un único riesgo clínico conjunto.

Problema real que motiva esto: no todas las omisiones tienen el mismo impacto según el contexto. Olvidar una pastilla no crítica no es igual a olvidarla + no haber comido en 6 horas + estar además muy sedentario (posible indicio de malestar). El impacto real es **no lineal**: la combinación de señales moderadas puede ser más grave que cualquiera aislada.

## Decisión de alcance

Se agrega una **capa nueva encima** del motor difuso existente — no lo reemplaza:

- **Edge (sin cambios):** `crit.evaluar()` sigue decidiendo insistencia por actividad individual. Offline, sin dependencias, sigue corriendo en el dispositivo del paciente.
- **Cloud (nuevo):** módulo `backend/risk/` que combina evidencia de varias actividades + vitales en un solo `P(Descompensación)`, usando una red bayesiana con evidencia difusa (soft evidence). Corre en el backend cloud, no en edge — coherente con el split edge/cloud ya documentado en `[[stack-y-arquitectura]]`.

Ambas capas coexisten: la capa edge sigue generando recordatorios y alertas por actividad; la capa cloud añade una alerta adicional de "riesgo global" cuando la combinación de señales lo amerita, aunque ninguna señal individual haya escalado por sí sola.

## Componentes

### 1. `backend/risk/history.py`
Ajuste bayesiano simple (Beta-update / conteo de frecuencias) sobre la tabla `Event`: para cada nodo de evidencia, calcula la tasa histórica reciente (ventana de N días) de retrasos/rechazos de ese tipo de actividad, y la usa para ajustar el prior base del nodo antes de fuzzificar. No es un modelo de ML entrenado — es una actualización de conteos clásica (funciona incluso con poco historial: si no hay datos, cae al prior por defecto).

### 2. `backend/risk/evidence.py`
Traduce el estado actual del paciente en tres evidencias difusas [0-1], reutilizando las funciones de pertenencia ya existentes en `crit` (`_tri`, `_grade_up`):

| Nodo | Eje temporal | Fuente de datos |
|---|---|---|
| `olvido_medicacion` | Agudo (horas) | Actividades tipo `medicacion` + retraso |
| `ayuno` | Subagudo (días) | Actividades tipo `comida` + retraso |
| `sedentarismo` | Crónico (semanas) | Pasos de hoy (`Vital`) vs. baseline histórico del paciente |

### 3. `backend/risk/bayes_engine.py`
Red bayesiana con `pgmpy`. DAG: `olvido_medicacion → Descompensacion`, `ayuno → Descompensacion`, `sedentarismo → Descompensacion`. CPTs definidas a mano (no aprendidas), con mayor peso condicional a `olvido_medicacion` (coherente con el eje agudo > crónico), basadas en criterio clínico de `docs/investigacion/`.

Las evidencias difusas del paso 2 se inyectan como **soft evidence** (`virtual_evidence` de pgmpy) — el grado de membresía pesa la inferencia, no solo un estado binario "sí/no". Inferencia exacta vía `VariableElimination`.

### 4. Salida y alertas
`P(Descompensación)` se mapea a 4 niveles (tabla acordada):

| P(Descomp) | Estado | Acción |
|---|---|---|
| < 30% | Rutina alterada pero segura | Ninguna / log |
| 30–60% | Riesgo preventivo | Alerta suave al familiar |
| 60–85% | Riesgo agudo moderado | Alerta sonora / notificación urgente |
| > 85% | Crisis inminente | Alarma roja a cuidador + contactos de emergencia |

Se crea una `Alerta` (mismo modelo, sin campo `tipo` — el modelo actual no lo tiene) con `actividad_id=None` y `motivo="Riesgo global {tier}: ..."` — el prefijo en `motivo` distingue esta alerta de las que ya genera `routine/engine.py` por actividad puntual (`motivo="No se completó: {nombre}"`), para que el cuidador distinga "esta actividad no se hizo" de "el conjunto de señales sugiere riesgo real".

## Flujo de datos

Nuevo endpoint `POST /riesgo/{patient_id}/evaluar` (se llama junto a `procesar_pendientes`, o vía cron cada N horas):

1. Lee `Actividad`, `Vital`, `Event` recientes del paciente.
2. `history.py` ajusta los priors de cada nodo según historial reciente.
3. `evidence.py` fuzzifica las 3 señales actuales.
4. `bayes_engine.py` infiere `P(Descompensación)` con soft evidence.
5. Se genera una traza explicable (qué nodo pesó más — mismo espíritu que la traza ya existente en `crit.evaluar`).
6. Si el tier ≥ preventivo, se crea la `Alerta` correspondiente.

Ejemplo de no-linealidad esperado (el caso que motivó este diseño): olvido de medicación + 6h de ayuno simultáneos deben producir un salto de riesgo mayor que la suma lineal de ambas señales aisladas — esto es lo que la CPT conjunta de la red bayesiana captura y una simple suma ponderada no.

## Manejo de límites

- Paciente nuevo sin historial: `history.py` devuelve el prior default (CPT base sin ajuste) — no falla, no bloquea.
- `pgmpy` es dependencia nueva, solo usada en `backend/risk/` (capa cloud). Si el módulo falla o no está instalado, el motor edge (`crit.evaluar`, recordatorios, confirmación) sigue funcionando intacto — el offline-first del sistema no depende de esta capa.

## Testing

Mismo patrón que los tests ya existentes de `crit.evaluar` (casos fijos, sin mocks pesados):

- Todo normal → P(Descomp) < 30%.
- Olvido de medicación + ayuno + sedentarismo simultáneos → > 85% (verifica el salto no-lineal, caso central de este diseño).
- Una sola señal alta y aislada → tier medio, no escala a crisis por sí sola (verifica que el sistema no sobre-alerta por una señal única, requisito original del pivote de "no controlar todo").
- Paciente sin historial (`Event` vacío) → usa prior default, no lanza error.
