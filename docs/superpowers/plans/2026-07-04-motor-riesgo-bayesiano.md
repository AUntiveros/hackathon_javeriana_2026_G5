# Motor de riesgo global (Fuzzy-Bayesian Network) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Agregar una capa cloud nueva (`backend/risk/`) que combina evidencia difusa de varias actividades y vitales del paciente en un único `P(Descompensación)` vía red bayesiana (pgmpy), sin modificar el motor de criticidad por-actividad existente (`backend/criticality/engine.py`).

**Architecture:** Dos capas independientes. Edge (sin cambios): `crit.evaluar()` sigue decidiendo insistencia por actividad individual. Cloud (nuevo): `backend/risk/evidence.py` fuzzifica 3 señales (olvido de medicación, ayuno, sedentarismo), `backend/risk/history.py` las ajusta con la tasa histórica de incumplimiento (Beta-Bernoulli sobre `Actividad`, sin ML entrenado), `backend/risk/bayes_engine.py` las combina con una red bayesiana de 3 nodos padre → 1 nodo `descompensacion` usando evidencia blanda (`virtual_evidence` de pgmpy), y `backend/risk/engine.py` orquesta todo, mapea a 4 niveles de alerta y crea `Alerta(tipo="riesgo_global")` cuando corresponde.

**Tech Stack:** Python 3.13, FastAPI, SQLModel/SQLite, `pgmpy` 1.1.2 (`DiscreteBayesianNetwork`, `TabularCPD`, `VariableElimination`), `pytest` (nuevo, el proyecto no tenía suite de tests — antes solo verificación manual con `TestClient`).

## Global Constraints

- No modificar `backend/criticality/engine.py` ni `backend/routine/engine.py` — el motor por-actividad sigue igual, edge/offline, sin dependencias nuevas.
- Las dependencias nuevas (`pgmpy`, `pytest`) solo se usan en `backend/risk/` y sus tests — no deben importarse desde módulos edge/offline (`backend/edge/demo_offline.py`, `backend/criticality/`).
- Todo output de riesgo debe incluir traza explicable (los 3 grados de evidencia usados), igual que la traza que ya expone `crit.evaluar()`.
- Ver spec completo en `docs/superpowers/specs/2026-07-04-motor-riesgo-bayesiano-design.md`.
- **Nota destructiva:** `backend/app.db` ya existe con el schema viejo de `Vital` (sin columna `pasos`). SQLAlchemy `create_all()` NO agrega columnas a tablas existentes. La Tarea 2 requiere borrar `backend/app.db` y correr `python -m backend.db.seed` de nuevo para que el nuevo schema tome efecto. Es la base de datos de demo (se regenera con el seed), pero confirmar con el usuario antes de borrar si hay datos de prueba que no estén en el seed.

---

### Task 1: Dependencias nuevas (`pgmpy`, `pytest`)

**Files:**
- Modify: `backend/requirements.txt`

**Interfaces:**
- Produces: `pgmpy` y `pytest` disponibles para todas las tareas siguientes.

- [ ] **Step 1: Agregar las dependencias al final de `backend/requirements.txt`**

```
# Motor de riesgo global (fuzzy-bayesiano)
pgmpy

# Testing
pytest
```

- [ ] **Step 2: Instalar**

Run: `pip install pgmpy pytest`
Expected: `Successfully installed ... pgmpy-1.1.2 ... pytest-...` (ya están instalados en este entorno; en uno nuevo, instala ambos)

- [ ] **Step 3: Verificar import**

Run: `python -c "from pgmpy.models import DiscreteBayesianNetwork; import pytest; print('ok')"`
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add backend/requirements.txt
git commit -m "chore: agregar pgmpy y pytest para el motor de riesgo global"
```

---

### Task 2: Campo `pasos` en `Vital` (modelo + endpoint)

El motor de riesgo necesita pasos diarios del smartwatch para el nodo de sedentarismo; el modelo `Vital` hoy solo guarda `hr`/`hrv_ms`/`bp_*`.

**Files:**
- Modify: `backend/db/models.py` (clase `Vital`, línea 61 — después de `hrv_ms`)
- Modify: `backend/main.py` (`VitalIn`, `ingest_vital`, `listar_vitals`, líneas 138–163)
- Test: `backend/db/test_vital_pasos.py`

**Interfaces:**
- Produces: `Vital.pasos: int`, `POST /vitals` acepta `pasos` en el body, `GET /vitals/{pid}` lo devuelve.

- [ ] **Step 1: Escribir el test que falla**

Crear `backend/db/test_vital_pasos.py`:

```python
from fastapi.testclient import TestClient
from sqlmodel import select

from backend.db.models import Vital, get_session, init_db
from backend.main import app

PID = 999998
client = TestClient(app)


def _limpiar():
    with get_session() as s:
        for v in s.exec(select(Vital).where(Vital.patient_id == PID)).all():
            s.delete(v)
        s.commit()


def test_ingest_vital_guarda_y_devuelve_pasos():
    init_db()
    _limpiar()
    r = client.post("/vitals", json={"patient_id": PID, "hr": 70, "hrv_ms": 40.0, "pasos": 1234})
    assert r.status_code == 200
    r2 = client.get(f"/vitals/{PID}")
    assert r2.json()[0]["pasos"] == 1234
    _limpiar()
```

- [ ] **Step 2: Correr el test para verificar que falla**

Run: `pytest backend/db/test_vital_pasos.py -v`
Expected: FAIL — `pydantic`/`KeyError: 'pasos'` (el campo no existe todavía) o, si `backend/app.db` ya existe con schema viejo, `sqlite3.OperationalError: no such column: vital.pasos` (ver nota destructiva arriba)

- [ ] **Step 3: Agregar el campo al modelo**

En `backend/db/models.py`, clase `Vital` (después de la línea `hrv_ms: float = 0.0`):

```python
    hrv_ms: float = 0.0
    pasos: int = 0                     # pasos del dia (podometro del smartwatch)
```

- [ ] **Step 4: Actualizar el endpoint en `backend/main.py`**

`VitalIn` (línea ~138):

```python
class VitalIn(BaseModel):
    patient_id: int = 1
    hr: int
    hrv_ms: float = 0.0
    pasos: int = 0
```

`ingest_vital` (línea ~144):

```python
@app.post("/vitals")
def ingest_vital(body: VitalIn):
    with get_session() as s:
        p = s.exec(select(Patient).where(Patient.id == body.patient_id)).first()
        edad = p.edad if p else 75
        bp = estimate.estimar_presion(body.hr, body.hrv_ms, edad)
        v = Vital(patient_id=body.patient_id, hr=body.hr, hrv_ms=body.hrv_ms, pasos=body.pasos,
                  bp_sys_est=bp["bp_sys_est"], bp_dia_est=bp["bp_dia_est"])
        s.add(v)
        s.commit()
    return {"ok": True, **bp}
```

`listar_vitals` (línea ~157):

```python
@app.get("/vitals/{pid}")
def listar_vitals(pid: int, limit: int = 50):
    with get_session() as s:
        vs = s.exec(select(Vital).where(Vital.patient_id == pid)
                    .order_by(Vital.timestamp.desc())).all()
    return [{"ts": v.timestamp.isoformat(), "hr": v.hr, "hrv_ms": v.hrv_ms, "pasos": v.pasos,
             "bp_sys_est": v.bp_sys_est, "bp_dia_est": v.bp_dia_est} for v in vs[:limit]]
```

- [ ] **Step 5: Recrear la base para el nuevo schema**

Confirmar con el usuario, luego:

Run: `rm backend/app.db && python -m backend.db.seed`
Expected: `[seed] paciente + rutina del día cargados`

- [ ] **Step 6: Correr el test para verificar que pasa**

Run: `pytest backend/db/test_vital_pasos.py -v`
Expected: `1 passed`

- [ ] **Step 7: Commit**

```bash
git add backend/db/models.py backend/main.py backend/db/test_vital_pasos.py
git commit -m "feat: agregar pasos diarios a Vital (input del motor de riesgo global)"
```

---

### Task 3: `backend/risk/evidence.py` — fuzzificación de 3 señales

**Files:**
- Create: `backend/risk/__init__.py`
- Create: `backend/risk/evidence.py`
- Test: `backend/risk/test_evidence.py`

**Interfaces:**
- Consumes: `backend.criticality.engine._grade_up(x, a, b)` (ya existe, rampa creciente [0,1])
- Produces: `grado_olvido_medicacion(retraso_min: float) -> float`, `grado_ayuno(retraso_min: float) -> float`, `grado_sedentarismo(pasos_hoy: int, baseline: int) -> float` — usados por Task 6.

- [ ] **Step 1: Crear el paquete**

Crear `backend/risk/__init__.py` (vacío, mismo patrón que `backend/criticality/__init__.py`).

- [ ] **Step 2: Escribir el test que falla**

Crear `backend/risk/test_evidence.py`:

```python
from backend.risk import evidence


def test_grado_olvido_medicacion():
    assert evidence.grado_olvido_medicacion(0) == 0.0
    assert evidence.grado_olvido_medicacion(60) == 0.0
    assert evidence.grado_olvido_medicacion(180) == 1.0
    assert evidence.grado_olvido_medicacion(120) == 0.5


def test_grado_ayuno():
    assert evidence.grado_ayuno(0) == 0.0
    assert evidence.grado_ayuno(60) == 0.0
    assert evidence.grado_ayuno(240) == 1.0
    assert evidence.grado_ayuno(150) == 0.5


def test_grado_sedentarismo():
    assert evidence.grado_sedentarismo(1000, 1000) == 0.0
    assert evidence.grado_sedentarismo(500, 1000) == 0.5
    assert evidence.grado_sedentarismo(100, 1000) == 1.0
    assert evidence.grado_sedentarismo(500, 0) == 0.0  # sin baseline: no alarma falsa
```

- [ ] **Step 3: Correr el test para verificar que falla**

Run: `pytest backend/risk/test_evidence.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'backend.risk.evidence'`

- [ ] **Step 4: Implementar**

Crear `backend/risk/evidence.py`:

```python
"""Fuzzificación de evidencias para el motor de riesgo global (capa cloud).

Reutiliza las funciones de pertenencia del motor de criticidad por-actividad
(backend/criticality/engine.py) para mantener el mismo lenguaje difuso en ambas capas.
"""
from backend.criticality.engine import _grade_up


def grado_olvido_medicacion(retraso_min: float) -> float:
    """[0-1]: 60min de retraso ya es preocupante, 180min (3h) es 'olvido crítico'."""
    return _grade_up(retraso_min, 60, 180)


def grado_ayuno(retraso_min: float) -> float:
    """[0-1]: 60min sobre la ventana de la comida es 'retraso leve', 240min (4h) es ayuno severo."""
    return _grade_up(retraso_min, 60, 240)


def grado_sedentarismo(pasos_hoy: int, baseline: int) -> float:
    """[0-1]: cuánto cae pasos_hoy respecto al baseline histórico del paciente.
    Sin baseline (paciente nuevo, sin historial de vitales) -> 0.0, no genera falsa alarma."""
    if baseline <= 0:
        return 0.0
    caida = 1 - (pasos_hoy / baseline)
    return _grade_up(caida, 0.3, 0.7)
```

- [ ] **Step 5: Correr el test para verificar que pasa**

Run: `pytest backend/risk/test_evidence.py -v`
Expected: `4 passed`

- [ ] **Step 6: Commit**

```bash
git add backend/risk/__init__.py backend/risk/evidence.py backend/risk/test_evidence.py
git commit -m "feat: fuzzificacion de evidencias (olvido med, ayuno, sedentarismo) para riesgo global"
```

---

### Task 4: `backend/risk/history.py` — ajuste bayesiano simple (Beta-Bernoulli)

**Files:**
- Create: `backend/risk/history.py`
- Test: `backend/risk/test_history.py`

**Interfaces:**
- Consumes: `Actividad` (`backend.db.models`), campos `patient_id`, `tipo`, `fecha`, `estado`, `n_rechazos`.
- Produces: `tasa_historica(patient_id: int, tipo: str, dias: int = 7) -> float` — usado por Task 6.

- [ ] **Step 1: Escribir el test que falla**

Crear `backend/risk/test_history.py`:

```python
from datetime import date, timedelta

import pytest
from sqlmodel import select

from backend.db.models import Actividad, get_session, init_db
from backend.risk import history

PID = 999995  # paciente de prueba, no colisiona con el sembrado (id=1)


def _fecha(dias_atras: int) -> str:
    return (date.today() - timedelta(days=dias_atras)).isoformat()


def _limpiar():
    with get_session() as s:
        for a in s.exec(select(Actividad).where(Actividad.patient_id == PID)).all():
            s.delete(a)
        s.commit()


def test_sin_historial_devuelve_prior_neutro():
    init_db()
    _limpiar()
    assert history.tasa_historica(PID, "medicacion") == 0.5


def test_incumplimiento_historico_sube_la_tasa():
    init_db()
    _limpiar()
    with get_session() as s:
        for i in range(1, 6):
            s.add(Actividad(patient_id=PID, nombre="test", tipo="medicacion",
                             criticidad_base=0.9, hora="08:00", fecha=_fecha(i),
                             estado="pendiente"))
        s.commit()
    tasa = history.tasa_historica(PID, "medicacion")
    assert tasa == pytest.approx((5 + 1) / (5 + 2))
    _limpiar()


def test_cumplimiento_historico_baja_la_tasa():
    init_db()
    _limpiar()
    with get_session() as s:
        for i in range(1, 6):
            s.add(Actividad(patient_id=PID, nombre="test", tipo="medicacion",
                             criticidad_base=0.9, hora="08:00", fecha=_fecha(i),
                             estado="confirmada"))
        s.commit()
    tasa = history.tasa_historica(PID, "medicacion")
    assert tasa == pytest.approx((0 + 1) / (5 + 2))
    _limpiar()
```

- [ ] **Step 2: Correr el test para verificar que falla**

Run: `pytest backend/risk/test_history.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'backend.risk.history'`

- [ ] **Step 3: Implementar**

Crear `backend/risk/history.py`:

```python
"""Ajuste bayesiano simple (Beta-Bernoulli) de los priors del motor de riesgo global,
usando el historial de Actividad ya almacenado. Sin ML entrenado, sin Event nuevos:
el conteo de incumplimientos pasados de un tipo de actividad ES el historial.
"""
from datetime import date, timedelta

from sqlmodel import select

from backend.db.models import Actividad, get_session


def tasa_historica(patient_id: int, tipo: str, dias: int = 7) -> float:
    """Tasa Beta-Bernoulli (prior Beta(1,1)) de incumplimiento histórico de `tipo` de
    actividad en los últimos `dias` (excluye hoy). Sin historial -> 0.5 (prior neutro,
    ni bajo ni alto)."""
    hoy = date.today()
    desde = (hoy - timedelta(days=dias)).isoformat()
    hasta = (hoy - timedelta(days=1)).isoformat()
    with get_session() as s:
        acts = s.exec(
            select(Actividad).where(
                Actividad.patient_id == patient_id,
                Actividad.tipo == tipo,
                Actividad.fecha >= desde,
                Actividad.fecha <= hasta,
            )
        ).all()
    total = len(acts)
    incumplidas = sum(1 for a in acts if a.estado != "confirmada" or a.n_rechazos > 0)
    return (incumplidas + 1) / (total + 2)
```

- [ ] **Step 4: Correr el test para verificar que pasa**

Run: `pytest backend/risk/test_history.py -v`
Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/risk/history.py backend/risk/test_history.py
git commit -m "feat: ajuste bayesiano simple (Beta-Bernoulli) de historial para riesgo global"
```

---

### Task 5: `backend/risk/bayes_engine.py` — red bayesiana (pgmpy)

CPT calibrada y verificada numéricamente (no es una tabla arbitraria — se corrió con `VariableElimination` antes de escribir este plan): con las 3 señales altas simultáneas (0.9 cada una) el riesgo cruza el umbral de crisis (>85%); una sola señal alta y aislada se queda en preventivo (no escala sola). Ver `docs/superpowers/specs/2026-07-04-motor-riesgo-bayesiano-design.md`.

**Files:**
- Create: `backend/risk/bayes_engine.py`
- Test: `backend/risk/test_bayes_engine.py`

**Interfaces:**
- Consumes: `pgmpy.models.DiscreteBayesianNetwork`, `pgmpy.factors.discrete.TabularCPD`, `pgmpy.inference.VariableElimination` (nota: en pgmpy 1.1.2 la clase es `DiscreteBayesianNetwork`, NO `BayesianNetwork` — está deprecada y lanza `ImportError`).
- Produces: `inferir_riesgo(grado_olvido: float, grado_ayuno: float, grado_sedentarismo: float) -> float` — usado por Task 6.

- [ ] **Step 1: Escribir el test que falla**

Crear `backend/risk/test_bayes_engine.py`:

```python
import pytest

from backend.risk import bayes_engine


def test_todo_normal_riesgo_bajo():
    p = bayes_engine.inferir_riesgo(0.05, 0.05, 0.05)
    assert p < 0.30


def test_una_sola_senal_alta_no_escala_sola():
    p = bayes_engine.inferir_riesgo(0.9, 0.05, 0.05)
    assert 0.30 <= p < 0.60


def test_tres_senales_altas_simultaneas_cruzan_crisis():
    p = bayes_engine.inferir_riesgo(0.9, 0.9, 0.9)
    assert p > 0.85


def test_dos_senales_altas_quedan_en_rango_agudo_moderado():
    p = bayes_engine.inferir_riesgo(0.9, 0.9, 0.05)
    assert 0.60 <= p < 0.85


def test_valores_conocidos_exactos():
    assert bayes_engine.inferir_riesgo(0.05, 0.05, 0.05) == pytest.approx(0.056, abs=0.01)
    assert bayes_engine.inferir_riesgo(0.9, 0.9, 0.9) == pytest.approx(0.869, abs=0.01)
```

- [ ] **Step 2: Correr el test para verificar que falla**

Run: `pytest backend/risk/test_bayes_engine.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'backend.risk.bayes_engine'`

- [ ] **Step 3: Implementar**

Crear `backend/risk/bayes_engine.py`:

```python
"""Red bayesiana (pgmpy) que combina 3 evidencias difusas en P(Descompensacion).

Capa cloud sobre el motor de criticidad por-actividad (edge, sin cambios). Los grados
difusos de entrada [0-1] se inyectan como evidencia blanda (virtual evidence): con
priors uniformes (0.5/0.5) en los 3 nodos raíz, el grado p entra directamente como
P(nodo=1)=p en la posterior, sin distorsión.

CPT de 'descompensacion' calibrada a mano y verificada numéricamente (ver spec en
docs/superpowers/specs/2026-07-04-motor-riesgo-bayesiano-design.md) para que:
- una sola señal alta y aislada quede en tier preventivo (no escala sola)
- las 3 señales altas simultáneas crucen el umbral de crisis (>85%), demostrando
  el salto NO lineal frente a un promedio ponderado simple.
"""
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork

_NODOS_EVIDENCIA = ("olvido_medicacion", "ayuno", "sedentarismo")

# P(descompensacion=1 | olvido, ayuno, sedentarismo). Columnas en el orden que usa
# pgmpy para evidence=[o, a, s], evidence_card=[2,2,2]: itertools.product([0,1],[0,1],[0,1])
# -> (0,0,0) (0,0,1) (0,1,0) (0,1,1) (1,0,0) (1,0,1) (1,1,0) (1,1,1)
_CPT_DESCOMP = [
    [0.97, 0.92, 0.85, 0.62, 0.65, 0.38, 0.25, 0.01],  # descompensacion = 0
    [0.03, 0.08, 0.15, 0.38, 0.35, 0.62, 0.75, 0.99],  # descompensacion = 1
]


def _construir_modelo() -> DiscreteBayesianNetwork:
    modelo = DiscreteBayesianNetwork([(n, "descompensacion") for n in _NODOS_EVIDENCIA])
    cpds_evidencia = [TabularCPD(n, 2, [[0.5], [0.5]]) for n in _NODOS_EVIDENCIA]
    cpd_descomp = TabularCPD(
        "descompensacion", 2,
        values=_CPT_DESCOMP,
        evidence=list(_NODOS_EVIDENCIA),
        evidence_card=[2, 2, 2],
    )
    modelo.add_cpds(*cpds_evidencia, cpd_descomp)
    assert modelo.check_model()
    return modelo


_MODELO = _construir_modelo()
_INFERENCIA = VariableElimination(_MODELO)


def inferir_riesgo(grado_olvido: float, grado_ayuno: float, grado_sedentarismo: float) -> float:
    """Devuelve P(Descompensacion) en [0,1] combinando las 3 evidencias difusas."""
    virtual_evidence = [
        TabularCPD("olvido_medicacion", 2, [[1 - grado_olvido], [grado_olvido]]),
        TabularCPD("ayuno", 2, [[1 - grado_ayuno], [grado_ayuno]]),
        TabularCPD("sedentarismo", 2, [[1 - grado_sedentarismo], [grado_sedentarismo]]),
    ]
    resultado = _INFERENCIA.query(
        ["descompensacion"], virtual_evidence=virtual_evidence, show_progress=False
    )
    return float(resultado.values[1])
```

- [ ] **Step 4: Correr el test para verificar que pasa**

Run: `pytest backend/risk/test_bayes_engine.py -v`
Expected: `5 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/risk/bayes_engine.py backend/risk/test_bayes_engine.py
git commit -m "feat: red bayesiana (pgmpy) para combinar evidencias de riesgo global"
```

---

### Task 6: `backend/risk/engine.py` — orquestador (evidencia + historial + bayes → tier + alerta)

**Files:**
- Create: `backend/risk/engine.py`
- Test: `backend/risk/test_engine.py`

**Interfaces:**
- Consumes: `evidence.grado_olvido_medicacion`, `evidence.grado_ayuno`, `evidence.grado_sedentarismo` (Task 3); `history.tasa_historica` (Task 4); `bayes_engine.inferir_riesgo` (Task 5); `backend.routine.engine._hoy()`, `backend.routine.engine._retraso_min(hora, ventana)` (ya existen, reutilizados igual que en `backend/edge/demo_offline.py`); `Actividad`, `Alerta`, `Vital`, `get_session` (`backend.db.models`).
- Produces: `evaluar_riesgo_global(patient_id: int = 1) -> dict` con claves `patient_id`, `p_descompensacion`, `tier`, `evidencias` — usado por Task 7. También expone `_tier(p: float) -> str` y `_calcular_evidencias(patient_id: int) -> tuple[float, float, float]` (usados directamente en tests con monkeypatch).

- [ ] **Step 1: Escribir el test que falla**

Crear `backend/risk/test_engine.py`:

```python
from sqlmodel import select

from backend.db.models import Alerta, get_session, init_db
from backend.risk import engine

PID = 999996


def _limpiar():
    with get_session() as s:
        for a in s.exec(select(Alerta).where(Alerta.patient_id == PID)).all():
            s.delete(a)
        s.commit()


def test_tier_mapping():
    assert engine._tier(0.10) == "ninguna"
    assert engine._tier(0.45) == "preventivo"
    assert engine._tier(0.70) == "agudo_moderado"
    assert engine._tier(0.90) == "crisis"


def test_evaluar_riesgo_global_crea_alerta_en_crisis(monkeypatch):
    init_db()
    _limpiar()
    monkeypatch.setattr(engine, "_calcular_evidencias", lambda pid: (0.9, 0.9, 0.9))
    resultado = engine.evaluar_riesgo_global(PID)
    assert resultado["tier"] == "crisis"
    assert resultado["p_descompensacion"] > 0.85
    with get_session() as s:
        alertas = s.exec(select(Alerta).where(Alerta.patient_id == PID)).all()
    assert len(alertas) == 1
    assert alertas[0].nivel == "alto"
    _limpiar()


def test_evaluar_riesgo_global_no_crea_alerta_si_normal(monkeypatch):
    init_db()
    _limpiar()
    monkeypatch.setattr(engine, "_calcular_evidencias", lambda pid: (0.05, 0.05, 0.05))
    resultado = engine.evaluar_riesgo_global(PID)
    assert resultado["tier"] == "ninguna"
    with get_session() as s:
        alertas = s.exec(select(Alerta).where(Alerta.patient_id == PID)).all()
    assert len(alertas) == 0
    _limpiar()
```

- [ ] **Step 2: Correr el test para verificar que falla**

Run: `pytest backend/risk/test_engine.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'backend.risk.engine'`

- [ ] **Step 3: Implementar**

Crear `backend/risk/engine.py`:

```python
"""Motor de riesgo global — capa cloud que combina varias actividades y vitales del
paciente en un P(Descompensacion) único vía red fuzzy-bayesiana, SIN reemplazar el
motor de criticidad por-actividad existente (backend/criticality/engine.py sigue
decidiendo insistencia individual, edge, sin cambios).
"""
from datetime import date, timedelta

from sqlmodel import select

from backend.db.models import Actividad, Alerta, Vital, get_session
from backend.risk import bayes_engine, evidence, history
from backend.routine.engine import _hoy, _retraso_min

PESO_HISTORIAL = 0.3  # cuanto pesa la tendencia historica frente a la señal de hoy

_TIERS = (
    (0.30, "ninguna"),
    (0.60, "preventivo"),
    (0.85, "agudo_moderado"),
    (1.01, "crisis"),
)


def _tier(p: float) -> str:
    for limite, nombre in _TIERS:
        if p < limite:
            return nombre
    return "crisis"


def _peor_retraso(acts: list[Actividad], tipo: str) -> float:
    candidatas = [a for a in acts if a.tipo == tipo]
    if not candidatas:
        return 0.0
    return max(_retraso_min(a.hora, a.ventana_min) for a in candidatas)


def _pasos_hoy_y_baseline(patient_id: int) -> tuple[int, int]:
    hoy = _hoy()
    desde = (date.today() - timedelta(days=7)).isoformat()
    with get_session() as s:
        vitals = s.exec(select(Vital).where(Vital.patient_id == patient_id)).all()
    de_hoy = [v for v in vitals if v.timestamp.date().isoformat() == hoy]
    pasados = [v for v in vitals if desde <= v.timestamp.date().isoformat() < hoy]
    pasos_hoy = max((v.pasos for v in de_hoy), default=0)
    baseline = round(sum(v.pasos for v in pasados) / len(pasados)) if pasados else pasos_hoy
    return pasos_hoy, baseline


def _calcular_evidencias(patient_id: int) -> tuple[float, float, float]:
    hoy = _hoy()
    with get_session() as s:
        acts = s.exec(
            select(Actividad).where(Actividad.patient_id == patient_id, Actividad.fecha == hoy)
        ).all()

    retraso_med = _peor_retraso(acts, "medicacion")
    retraso_comida = _peor_retraso(acts, "comida")
    pasos_hoy, baseline = _pasos_hoy_y_baseline(patient_id)

    g_olvido = evidence.grado_olvido_medicacion(retraso_med)
    g_ayuno = evidence.grado_ayuno(retraso_comida)
    g_sedentarismo = evidence.grado_sedentarismo(pasos_hoy, baseline)

    hist_med = history.tasa_historica(patient_id, "medicacion")
    hist_comida = history.tasa_historica(patient_id, "comida")
    g_olvido = (1 - PESO_HISTORIAL) * g_olvido + PESO_HISTORIAL * hist_med
    g_ayuno = (1 - PESO_HISTORIAL) * g_ayuno + PESO_HISTORIAL * hist_comida

    return g_olvido, g_ayuno, g_sedentarismo


def _crear_alerta(patient_id: int, tier: str, p: float) -> None:
    nivel = "alto" if tier in ("agudo_moderado", "crisis") else "medio"
    with get_session() as s:
        s.add(Alerta(patient_id=patient_id, nivel=nivel,
                      motivo=f"Riesgo global {tier}: P(descompensacion)={p:.2f}"))
        s.commit()


def evaluar_riesgo_global(patient_id: int = 1) -> dict:
    g_olvido, g_ayuno, g_sedentarismo = _calcular_evidencias(patient_id)
    p = bayes_engine.inferir_riesgo(g_olvido, g_ayuno, g_sedentarismo)
    tier = _tier(p)

    if tier != "ninguna":
        _crear_alerta(patient_id, tier, p)

    return {
        "patient_id": patient_id,
        "p_descompensacion": round(p, 3),
        "tier": tier,
        "evidencias": {
            "olvido_medicacion": round(g_olvido, 3),
            "ayuno": round(g_ayuno, 3),
            "sedentarismo": round(g_sedentarismo, 3),
        },
    }
```

- [ ] **Step 4: Correr el test para verificar que pasa**

Run: `pytest backend/risk/test_engine.py -v`
Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/risk/engine.py backend/risk/test_engine.py
git commit -m "feat: orquestador de riesgo global (evidencia+historial+bayes -> tier+alerta)"
```

---

### Task 7: Endpoint `POST /riesgo/{pid}/evaluar`

**Files:**
- Modify: `backend/main.py` (import en línea 19, nuevo endpoint después de `reporte_jornada`, línea ~185)
- Test: `backend/risk/test_endpoint.py`

**Interfaces:**
- Consumes: `backend.risk.engine.evaluar_riesgo_global(patient_id: int) -> dict` (Task 6).
- Produces: endpoint HTTP `POST /riesgo/{pid}/evaluar` que devuelve el mismo dict.

- [ ] **Step 1: Escribir el test que falla**

Crear `backend/risk/test_endpoint.py`:

```python
from fastapi.testclient import TestClient
from sqlmodel import select

from backend.db.models import Alerta, get_session, init_db
from backend.main import app
from backend.risk import engine

PID = 999997
client = TestClient(app)


def _limpiar():
    with get_session() as s:
        for a in s.exec(select(Alerta).where(Alerta.patient_id == PID)).all():
            s.delete(a)
        s.commit()


def test_endpoint_riesgo_evaluar_devuelve_tier_crisis(monkeypatch):
    init_db()
    _limpiar()
    monkeypatch.setattr(engine, "_calcular_evidencias", lambda pid: (0.9, 0.9, 0.9))
    r = client.post(f"/riesgo/{PID}/evaluar")
    assert r.status_code == 200
    body = r.json()
    assert body["tier"] == "crisis"
    assert body["patient_id"] == PID
    _limpiar()
```

- [ ] **Step 2: Correr el test para verificar que falla**

Run: `pytest backend/risk/test_endpoint.py -v`
Expected: FAIL — `404 Not Found` (el endpoint no existe todavía)

- [ ] **Step 3: Agregar el import y el endpoint en `backend/main.py`**

Agregar el import (junto a los demás, línea 19):

```python
from backend.risk import engine as risk_engine
```

Agregar el endpoint después de `reporte_jornada` (línea ~185, antes de la sección `# ---------- Personalización cultural`):

```python
# ---------- Riesgo global (fuzzy-bayesiano, capa cloud) ----------
@app.post("/riesgo/{pid}/evaluar")
def riesgo_evaluar(pid: int):
    return risk_engine.evaluar_riesgo_global(pid)
```

- [ ] **Step 4: Correr el test para verificar que pasa**

Run: `pytest backend/risk/test_endpoint.py -v`
Expected: `1 passed`

- [ ] **Step 5: Correr toda la suite de `backend/risk/` + el test de vitales para verificar que nada se rompió**

Run: `pytest backend/risk/ backend/db/test_vital_pasos.py -v`
Expected: `16 passed` (3 evidence + 3 history + 5 bayes_engine + 3 engine + 1 endpoint + 1 vital_pasos)

- [ ] **Step 6: Commit**

```bash
git add backend/main.py backend/risk/test_endpoint.py
git commit -m "feat: endpoint POST /riesgo/{pid}/evaluar para el motor de riesgo global"
```

---

## Post-plan (no incluido, roadmap para el pitch)

- Frontend: consumir `/riesgo/{pid}/evaluar` en la vista del equipo (médico/cuidador) para mostrar el nivel de riesgo global junto a las alertas por actividad. No incluido aquí — el terreno de "frontend components" lo lleva la terminal del frontend según `[[estado-implementacion]]`.
- Llamar `evaluar_riesgo_global` automáticamente (cron o junto a `procesar_pendientes`) en vez de requerir una llamada manual al endpoint — se dejó manual a propósito en este plan para no acoplar el ciclo de vida al motor edge existente.
