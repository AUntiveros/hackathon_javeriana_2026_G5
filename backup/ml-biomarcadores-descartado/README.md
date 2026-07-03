# Track ML — Biomarcadores de voz + contexto SES (Alzheimer, español)

Pipeline que prueba la hipótesis **`P(AD | Voz, Contexto SES)` vs `P(AD | Voz)`**:
la metadata socioeconómica (escolaridad, zona, IDH, lengua) aproxima la **reserva
cognitiva** y debe reducir el sobre-diagnóstico en poblaciones de baja escolaridad.

## Reproducir

```bash
cd ml
python -m venv .venv && . .venv/Scripts/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download es_core_news_sm              # o es_core_news_lg (mejor, +pesado)

python 00_download.py     # dataset -> data/raw.parquet  (+ manifest.json)
python 01_features.py     # features -> data/features.parquet
python 02_baseline.py     # P(AD|Voz)       -> results/baseline_metrics.json
python 03_ses_model.py    # P(AD|Voz,SES)   -> results/ses_metrics.json  (+ DELTA)
python 04_fairness.py     # fairness/CSVs/PNGs por escolaridad
python 05_export.py       # model.pkl + feature_schema.json + model_card.md
```

Los pasos 00→05 son **secuenciales** (cada uno lee la salida del anterior).

## Estado del dataset (IMPORTANTE)

**MultiConAD no está accesible públicamente en HuggingFace** al 2026-07-02 (la búsqueda
en el Hub devuelve 0 resultados; los `dementiabank` que aparecen son inglés/Pitt, no
español, y las features léxicas **no transfieren** cross-lingual). El pipeline corre por
tanto sobre el **fallback SINTÉTICO documentado** (`common.synthesize_feature_matrix`):
una matriz de features con un **confound de reserva cognitiva inyectado a propósito**.
Es una **prueba de concepto del mecanismo**, no una medición sobre habla real.

- Si consigues el ID/acceso correcto de MultiConAD: `MULTICONAD_ID=<repo_id> python 00_download.py`.
- Upgrade real: Ivanova Corpus (DementiaBank/TalkBank, 361 sujetos ES con nivel educativo).
- Con audio real: activar bloque acústico (librosa/parselmouth/webrtcvad) en `01_features.py`
  (correr en Colab por Whisper).

Todo el pipeline es **agnóstico al origen**: cuando llegue data real (texto o audio),
`01_features.py` extrae features reales y 02–05 corren sin cambios.

## Contrato con el backend

`model.pkl` = `{pipeline (StandardScaler+clf), features, threshold, positive_label}`.
`feature_schema.json` = orden exacto de features. **`backend/biomarkers/extract.py` debe
producir `speech_features` en ese orden**; las `ses_features` vienen de la metadata del
paciente. Clasificadores primarios: **XGBoost/RandomForest** (evidencia MultiConAD: el
español rinde mejor con árboles); SVM-RBF solo como referencia.

## Resumen para el pitch (5 líneas) — resultados sobre data sintética

1. **Baseline (solo voz)** CV 5-fold: AUC 0.746, F1 0.68, sens 0.68, espec 0.69.
2. **El baseline SOBRE-DIAGNOSTICA baja escolaridad**: FPR 0.41 en escolaridad baja vs
   0.25 en alta — el confound de reserva hace que un adulto sano de baja escolaridad
   "suene" a deterioro.
3. **Añadir SES como covariable cruda** mejora poco (AUC +0.004) y **no corrige** el FPR
   de baja escolaridad: el árbol no "descuenta" el confound solo por tener la feature
   (hallazgo honesto e importante).
4. **La forma efectiva de usar el contexto SES es calibración por grupo** (umbral por
   escolaridad, técnica de Equalized Odds): baja el FPR de baja escolaridad de **0.41 → 0.27**
   (iguala al grupo aventajado), con un costo documentado de sensibilidad (0.65 → 0.54).
5. **Frase de impacto:** *"un modelo agnóstico al contexto clasifica mal a un adulto mayor
   quechuahablante de baja escolaridad; añadir metadata SES —bien usada, vía calibración por
   grupo— reduce ese falso positivo."*

> Delta pequeño en AUC: esperado y honesto. El valor de SES no está en el AUC global sino
> en la **equidad** (cerrar FPR/sensibilidad entre grupos). Con data real (Ivanova, con
> educación medida) el efecto podría diferir — este pipeline queda listo para medirlo.

Artefactos: `results/roc_comparison.png`, `results/fpr_by_education.png`,
`results/feature_importance.png`, `results/metrics_comparison.csv`,
`results/fairness_by_education.csv`, `model_card.md`.
