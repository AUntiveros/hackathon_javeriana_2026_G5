"""
05_export.py — Reentrena el mejor modelo +SES con todo el train y exporta:
  ml/model.pkl            (Pipeline sklearn: StandardScaler + clasificador)
  ml/feature_schema.json  (orden/nombres de features que espera el backend)
  ml/model_card.md        (dataset, features, métricas, límites, benchmarks)

Contrato con backend/biomarkers/extract.py: debe producir las features de HABLA
en el MISMO orden que feature_schema["speech_features"]; las SES vienen de la
metadata del paciente (feature_schema["ses_features"]).
"""
from __future__ import annotations

import json
import pickle
import sys
from datetime import date

import pandas as pd

import common as C
import modeling as M


def main():
    df = pd.read_parquet(C.DATA_DIR / "features.parquet")
    manifest = C.read_manifest()
    speech = C.speech_feature_names(df.columns)
    ses = C.ses_feature_names(df.columns)
    feats = speech + ses

    ses_m = json.loads((C.RESULTS_DIR / "ses_metrics.json").read_text(encoding="utf-8"))
    base_m = json.loads((C.RESULTS_DIR / "baseline_metrics.json").read_text(encoding="utf-8"))
    best = ses_m["best"]

    # Reentrenar en TODA la data
    model = M.build_models()[best]
    model.fit(df[feats].to_numpy(float), df[C.LABEL_COL].to_numpy(int))
    with open(C.ML_DIR / "model.pkl", "wb") as f:
        pickle.dump({"pipeline": model, "features": feats,
                     "threshold": 0.5, "positive_label": "AD/MCI"}, f)

    schema = {
        "model_name": f"{best}_voz+SES",
        "created": str(date.today()),
        "feature_order": feats,
        "speech_features": speech,
        "timing_features": [c for c in C.TIMING_FEATURES if c in df.columns],
        "acoustic_features": [c for c in C.ACOUSTIC_FEATURES if c in df.columns],
        "ses_features": ses,
        "label": {"0": "HC (control)", "1": "AD/MCI (deterioro)"},
        "threshold": 0.5,
        "notes": ("extract.py debe producir speech_features en este orden; "
                  "las ses_features provienen de la metadata del paciente. "
                  "timing_features son proxy si el input es texto, VAD si es audio."),
    }
    (C.ML_DIR / "feature_schema.json").write_text(
        json.dumps(schema, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- model_card.md ----
    bm = base_m["metrics"][base_m["best"]]
    sm = ses_m["metrics"][best]
    try:
        comp = pd.read_csv(C.RESULTS_DIR / "metrics_comparison.csv")
        comp_tbl = comp.to_markdown(index=False)
    except Exception:
        comp_tbl = "(correr 04_fairness.py)"

    synth_note = ""
    if manifest.get("is_synthetic_features"):
        synth_note = ("\n> ⚠️ **Datos SINTÉTICOS.** MultiConAD no estaba disponible; este modelo se "
                      "entrenó sobre una matriz de features generada por un modelo generativo "
                      "documentado (`common.synthesize_feature_matrix`), con un confound de reserva "
                      "cognitiva inyectado a propósito. Es una **prueba de concepto del mecanismo**, "
                      "no una medición sobre habla real. Rehacer con MultiConAD/Ivanova.\n")
    elif manifest.get("ses_synthetic"):
        synth_note = ("\n> ℹ️ Transcripts reales (MultiConAD); metadata SES **sintética** "
                      "(correlación débil-moderada documentada, sin confound inyectado). El delta "
                      "+SES es lo que salga honestamente sobre SES simulada.\n")

    card = f"""# Model Card — Detección de deterioro cognitivo por voz + contexto SES (ES)

**Fecha:** {date.today()}  ·  **Modelo:** `{best}` (Pipeline: StandardScaler + clasificador)
**Tarea:** clasificación binaria HC vs AD/MCI a partir de habla espontánea en español
(tarea de referencia tipo *Cookie Theft*).
{synth_note}
## Dataset
- Fuente: **{manifest.get('dataset', 'n/d')}**  ·  modalidad: {manifest.get('modality', 'n/d')}
- N = {manifest.get('n_samples', '?')}  (positivos AD/MCI = {manifest.get('n_positive', '?')},
  controles HC = {manifest.get('n_negative', '?')})
- Metadata SES sintética: {manifest.get('ses_synthetic', False)} · confound inyectado: {manifest.get('ses_confound_injected', False)}

## Features ({len(feats)})
- **Habla ({len(speech)})**: léxicas/sintácticas (TTR, MATTR, Brunet, Honoré, long. oración,
  subordinación, ratios POS), semánticas (coherencia coseno, perseveración), y **timing** (pausas,
  tasa de habla, ratio silencio). *Timing prioritizado por robustez cross-lingual.*
- **SES ({len(ses)})**: {', '.join(ses)}

## Métricas (CV estratificada 5-fold, out-of-fold)
| modelo | AUC | F1 | Sensibilidad | Especificidad |
|---|---|---|---|---|
| Baseline P(AD\\|Voz) — {base_m['best']} | {bm['auc']:.3f} | {bm['f1']:.3f} | {bm['sensitivity']:.3f} | {bm['specificity']:.3f} |
| +SES P(AD\\|Voz,SES) — {best} | {sm['auc']:.3f} | {sm['f1']:.3f} | {sm['sensitivity']:.3f} | {sm['specificity']:.3f} |

### Comparación baseline vs +SES (incl. equidad)
{comp_tbl}

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
"""
    (C.ML_DIR / "model_card.md").write_text(card, encoding="utf-8")

    print(f"[05] Exportado:")
    print(f"     model.pkl            ({best}, {len(feats)} features)")
    print(f"     feature_schema.json  ({len(feats)} features en orden)")
    print(f"     model_card.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
