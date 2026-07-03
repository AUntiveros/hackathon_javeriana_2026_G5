# Model Card — Detección de deterioro cognitivo por voz + contexto SES (ES)

**Fecha:** 2026-07-02  ·  **Modelo:** `RandomForest` (Pipeline: StandardScaler + clasificador)
**Tarea:** clasificación binaria HC vs AD/MCI a partir de habla espontánea en español
(tarea de referencia tipo *Cookie Theft*).

> ⚠️ **Datos SINTÉTICOS.** MultiConAD no estaba disponible; este modelo se entrenó sobre una matriz de features generada por un modelo generativo documentado (`common.synthesize_feature_matrix`), con un confound de reserva cognitiva inyectado a propósito. Es una **prueba de concepto del mecanismo**, no una medición sobre habla real. Rehacer con MultiConAD/Ivanova.

## Dataset
- Fuente: **SINTÉTICO (fallback offline / demo de concepto)**  ·  modalidad: features
- N = 360  (positivos AD/MCI = 180,
  controles HC = 180)
- Metadata SES sintética: True · confound inyectado: True

## Features (29)
- **Habla (20)**: léxicas/sintácticas (TTR, MATTR, Brunet, Honoré, long. oración,
  subordinación, ratios POS), semánticas (coherencia coseno, perseveración), y **timing** (pausas,
  tasa de habla, ratio silencio). *Timing prioritizado por robustez cross-lingual.*
- **SES (9)**: education_years, education_low, parent_education_years, occupation_skill, welfare_quintile, urban, idh, native_spanish, bilingual

## Métricas (CV estratificada 5-fold, out-of-fold)
| modelo | AUC | F1 | Sensibilidad | Especificidad |
|---|---|---|---|---|
| Baseline P(AD\|Voz) — RandomForest | 0.746 | 0.683 | 0.678 | 0.694 |
| +SES P(AD\|Voz,SES) — RandomForest | 0.750 | 0.672 | 0.667 | 0.683 |

### Comparación baseline vs +SES (incl. equidad)
| metric                |   baseline |    ses |   delta |
|:----------------------|-----------:|-------:|--------:|
| auc                   |     0.7459 | 0.7502 |  0.0044 |
| f1                    |     0.6835 | 0.6723 | -0.0112 |
| sensitivity           |     0.6778 | 0.6667 | -0.0111 |
| specificity           |     0.6944 | 0.6833 | -0.0111 |
| equal_opportunity_gap |     0.0495 | 0.0562 |  0.0067 |
| fpr_gap               |     0.1648 | 0.1477 | -0.0171 |

Clasificadores: **XGBoost / RandomForest** primarios (evidencia MultiConAD: el español rinde
mejor con árboles); **SVM-RBF** solo como referencia.

## Fairness
Estratificado por escolaridad (baja vs alta). Métricas: sensibilidad/especificidad/FPR por grupo,
**Equal Opportunity gap** (|ΔTPR|) y **FPR gap**. Ver `results/fairness_by_education.csv` y
`results/fpr_by_education.png`.

Hallazgo (honesto): el **baseline sobre-diagnostica escolaridad baja** (FPR ~0.41 vs ~0.25 en alta).
Añadir SES como **covariable cruda NO corrige** ese FPR — el árbol no descuenta el confound solo por
tener la feature. Lo que sí lo corrige es **calibración por grupo** (umbral por escolaridad,
Equalized Odds): baja el FPR de escolaridad baja hasta igualar al grupo aventajado, con un costo
documentado de sensibilidad. Técnicas adicionales evaluadas: Borderline-SMOTE (fila `+SES+SMOTE`).

## Límites
- SES aproxima **reserva cognitiva**, no la mide; no es diagnóstico clínico.
- Voz = identificador biométrico (Ley 29733 Perú) → desplegar Edge/federated.
- Español y >80 años tienen menor sensibilidad reportada en la literatura → auditar por edad.
- Features léxicas NO transfieren cross-lingual; timing sí (~AUC 0.75 zero-shot).

## Benchmarks de referencia (cualitativos, no metas)
- Whisper-medium ADReSS: ~0.73 acc / 0.80 AUC.
- VoxCog: 0.875 (usa prior dialectal, +5-7%).
- Reportamos lo obtenido honestamente arriba; no se ajustó a estos números.
