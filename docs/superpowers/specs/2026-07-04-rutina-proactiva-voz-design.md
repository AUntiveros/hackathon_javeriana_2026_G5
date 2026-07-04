# Rutina proactiva + confirmación por voz + limpieza de roles — Diseño

## Contexto

El backend ya tiene un motor de rutina completo (`backend/routine/engine.py`) y un motor de
criticidad difuso (`backend/criticality/engine.py`) con sus endpoints (`/routine`, `/actividades/*`,
`/alertas/*`), pero el **frontend nunca los llama** — `client.ts` define `procesarRutina`,
`confirmarActividad`, `rechazarActividad`, `getAlertas`, pero ningún hook/vista los usa. `CuidadorView`
sigue en endpoints v1 sin mostrar alertas.

Este documento cubre la capa de **experiencia** que falta para probar de punta a punta los casos de
uso pedidos: preguntar por pastillas pendientes con detalle, sugerir actividad física, avisos
proactivos por horario, y confirmación de toma de pastilla por voz.

**Fuera de alcance (track paralelo, no tocar):** el diseño del motor de riesgo bayesiano
(`docs/superpowers/specs/2026-07-04-motor-riesgo-bayesiano-design.md`, capa `backend/risk/` sobre
`Vital`/`Event`) se está implementando por separado y se mantiene tal cual. Este spec no modifica
`backend/criticality/engine.py` ni crea `backend/risk/*`; la vista de alertas del cuidador se diseña
para ser compatible con que ese track agregue después un campo `tipo` a `Alerta` (hoy no existe, no
se agrega aquí).

## Hallazgo que define el diseño

El motor difuso decide **cuánta insistencia** aplicar a algo ya vencido/atrasado (con retraso=0
siempre devuelve `soltar`). No sirve para el aviso puntual "son las 2pm, toca almuerzo". Se necesitan
dos mecanismos separados y complementarios, ambos client-side, sin tocar el motor:

1. **Aviso puntual** (nuevo): al entrar la hora programada de una actividad `pendiente`, avisar una
   vez, sin pasar por el motor difuso.
2. **Escalada por atraso** (ya existe en el backend): pasada la ventana de tolerancia, llamar
   `procesarRutina` para que el motor difuso decida insistencia y genere `Alerta` si corresponde.

## Componentes

### 1. Polling en `useAcompanante.ts`
Mientras Tito está encendido (`vivoRef.current`), un intervalo cada 90s:
- Llama `getActividadesHoy(PATIENT_ID)`. Por cada actividad `pendiente` cuya hora ya llegó (dentro de
  `[hora, hora+ventana_min]`) y no está en el set `avisadasHoy` (se resetea a medianoche) → Tito la
  anuncia (mensaje neutro tipo `"Ya es hora de <nombre>"`, reusando la lógica de mensajes cálidos que
  ya existe en `routine/engine.py`) y la marca avisada.
- Llama `procesarRutina(PATIENT_ID)`. Por cada recordatorio con `accion !== 'soltar'` no avisado en
  los últimos 15 min (cooldown por `actividad_id`) → Tito dice `mensaje` (ya viene armado del backend).

### 2. Confirmación de pastilla por voz
Solo para `tipo === 'medicacion'`. Al avisar una, el hook entra en estado
`esperandoConfirmacion: { actividadId }`. La siguiente transcripción del paciente se evalúa primero
contra un matcher de palabras clave (determinístico, sin LLM):
- Coincide afirmativo (`sí|ya|listo|tomad[oa]`) → `confirmarActividad(id)`, Tito agradece, limpia el
  estado.
- Coincide negativo (`no|todavía no|aún no|no sé`) → `rechazarActividad(id)` (ya incrementa
  `n_rechazos` en el backend y re-evalúa con el motor difuso), Tito responde con calidez, arma cooldown
  de 15 min para re-avisar, limpia el estado de espera (no bloquea conversación).
- No coincide ninguno → no se llama a ningún endpoint; la frase sigue como conversación normal
  (`conversar()`); se reintentará en el siguiente ciclo de polling.

### 3. Contenido enriquecido (pastillas + actividad física)
- `Actividad.detalle` (JSON libre, ya existe en el modelo, sin migración) guarda
  `{"condicion": "hipertensión", "dosis_dia": 3}` para la pastilla de la presión, y
  `{"beneficio": "hipertensión", "pasos_meta": 1500}` para la caminata de la tarde.
- `_act_dict()` en `routine/engine.py` debe incluir `detalle` en lo que devuelve (hoy no lo hace) —
  sin esto el LLM nunca ve la condición ni la dosis.
- Seed (`backend/db/seed.py` + `backend/seed/don_manuel.json`): la pastilla de la presión pasa de
  1 toma/día a 3 (08:00, 14:00, 20:00) con el `detalle` de arriba.
- Requiere borrar `backend/app.db` y re-seedear (el seed no sobreescribe si el paciente ya existe;
  es dato de demo, sin pérdida real).
- System prompt del rol `paciente` (`orchestrator/agents.py`) se amplía: usar la rutina de hoy para
  responder con precisión sobre pastillas pendientes/tomadas/hora siguiente (contando filas del mismo
  nombre en el día), y sugerir la caminata pendiente con su beneficio cuando el paciente exprese que
  no sabe qué hacer / está aburrido.

### 4. Vista Cuidador
Migrar de v1 (`getRoutineToday`/`logMedicacion`) a v2 (`getActividadesHoy`/`confirmarActividad`) y
agregar una sección **Alertas**: `getAlertas(PATIENT_ID)` (refresco cada 60s) con nivel, motivo y
botón "Atender" → `atenderAlerta`. Se renderiza el campo `tipo` si viene presente en el payload (para
no romper cuando el track de riesgo bayesiano lo agregue), pero no se asume su existencia.

No se tocan `TwinDashboard`/`WearablePanel` en esta pasada — quedan para los cambios puntuales
posteriores que el usuario mencionó para Cuidador/Médico/Familiar.

### 5. Eliminar rol Comunidad
- Backend: quitar `ROLES["comunidad"]` de `orchestrator/agents.py`.
- Frontend: quitar de `RoleSelector.tsx`, `EquipoApp.tsx`, tipo `Rol` (`api/types.ts`), entradas en
  `mock.ts`; borrar `ComunidadView.tsx` + `comunidad.css`.

## Manejo de límites

- Sin conexión / STT no soportado: el polling y el aviso puntual siguen funcionando (usan
  `hablar()`/TTS, no dependen del reconocimiento); solo la confirmación por voz requiere STT — si no
  hay STT, el paciente puede confirmar con el input manual existente escribiendo "sí"/"no".
- Pantalla apagada / app cerrada: fuera de alcance (ver pregunta de acotación respondida — se asume
  pantalla siempre encendida, como ya está construido el modo acompañante).
- Coincidencia ambigua en la confirmación: se trata como "no confirmado todavía", no se penaliza
  (no cuenta como rechazo), se reintenta en el próximo ciclo.
- `app.db` no existe todavía / recién borrada: `init_db()` ya se llama en el startup de FastAPI, y
  `seed()` crea todo de cero sin error.

## Testing

- Manual end-to-end (es un prototipo de demo, no hay suite automatizada de este flujo todavía):
  1. Sembrar `app.db` limpio, arrancar backend, verificar `/routine/1/today` trae las 3 tomas de
     presión con `detalle`.
  2. Preguntar por voz/texto "¿qué pastillas tengo pendientes?" → la respuesta debe mencionar
     hipertensión, 3 veces al día, cuántas lleva y la hora de la siguiente.
  3. Decir "no sé qué hacer" → debe sugerir la caminata mencionando el beneficio para la presión.
  4. Esperar a que una actividad entre en su ventana horaria con la app abierta → Tito debe avisar
     sin que se le pregunte.
  5. Tras el aviso de una pastilla, responder "no" → debe confirmarse el rechazo, no marcarse tomada,
     y reintentar en ~15 min; repetir varias veces debe terminar generando una `Alerta` visible en
     Cuidador tras llamar `procesarRutina`.
  6. Verificar que el rol Comunidad ya no aparece en ningún selector ni responde por API.
