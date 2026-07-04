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
