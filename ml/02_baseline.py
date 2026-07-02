"""
02_baseline.py — Modelo P(AD|Voz): SOLO features del habla.

Entrena XGBoost, RandomForest (primarios) y SVM-RBF (referencia) con CV
estratificada 5-fold. Reporta AUC, F1, sensibilidad, especificidad.
Guarda OOF del mejor modelo primario para el análisis de fairness (04).
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

import common as C
import modeling as M


def report(title, results):
    print(f"\n===== {title} =====")
    print(f"{'modelo':<14}{'AUC':>7}{'F1':>7}{'Sens':>7}{'Spec':>7}   tipo")
    for name, (m, _) in results.items():
        tag = "árbol*" if name in M.PRIMARY_MODELS else "ref"
        print(f"{name:<14}{m['auc']:>7.3f}{m['f1']:>7.3f}"
              f"{m['sensitivity']:>7.3f}{m['specificity']:>7.3f}   {tag}")


def main():
    df = pd.read_parquet(C.DATA_DIR / "features.parquet")
    speech = C.speech_feature_names(df.columns)
    if not speech:
        print("[02] No hay features de habla."); return 1
    print(f"[02] Features de habla ({len(speech)}): {speech}")

    results = M.evaluate_all(df, speech)
    report("BASELINE  P(AD|Voz)", results)

    best = M.best_model_name(results)
    print(f"\n[02] Mejor modelo primario: {best}")

    # Persistir para 03/04
    metrics = {k: v[0] for k, v in results.items()}
    (C.RESULTS_DIR / "baseline_metrics.json").write_text(
        json.dumps({"best": best, "features": speech, "metrics": metrics},
                   indent=2), encoding="utf-8")
    np.savez(C.RESULTS_DIR / "oof_baseline.npz",
             oof=results[best][1], y=df[C.LABEL_COL].to_numpy(),
             education_low=df["education_low"].to_numpy() if "education_low" in df else np.zeros(len(df)),
             best=best)
    print(f"[02] Guardado -> results/baseline_metrics.json, oof_baseline.npz")
    return 0


if __name__ == "__main__":
    sys.exit(main())
