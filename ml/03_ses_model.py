"""
03_ses_model.py — Modelo P(AD|Voz, SES): features del habla + covariables SES.

Mismos algoritmos que el baseline, con las columnas SES añadidas. Reporta el
DELTA de cada métrica frente al baseline (02).
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

import common as C
import modeling as M


def main():
    df = pd.read_parquet(C.DATA_DIR / "features.parquet")
    speech = C.speech_feature_names(df.columns)
    ses = C.ses_feature_names(df.columns)
    if not ses:
        print("[03] No hay columnas SES; corre 00/01 primero."); return 1
    feats = speech + ses
    print(f"[03] Habla({len(speech)}) + SES({len(ses)}) = {len(feats)} features")
    print(f"[03] SES: {ses}")

    results = M.evaluate_all(df, feats)
    print("\n===== +SES  P(AD|Voz, SES) =====")
    print(f"{'modelo':<14}{'AUC':>7}{'F1':>7}{'Sens':>7}{'Spec':>7}")
    for name, (m, _) in results.items():
        print(f"{name:<14}{m['auc']:>7.3f}{m['f1']:>7.3f}"
              f"{m['sensitivity']:>7.3f}{m['specificity']:>7.3f}")

    best = M.best_model_name(results)
    print(f"\n[03] Mejor modelo primario +SES: {best}")

    # DELTA vs baseline
    base = json.loads((C.RESULTS_DIR / "baseline_metrics.json").read_text(encoding="utf-8"))
    print("\n===== DELTA (+SES − baseline), mismo modelo cuando existe =====")
    print(f"{'métrica':<14}{'baseline':>10}{'+SES':>10}{'delta':>10}")
    ses_best_m = results[best][0]
    base_ref = base["metrics"].get(best, base["metrics"][base["best"]])
    for k in ("auc", "f1", "sensitivity", "specificity"):
        d = ses_best_m[k] - base_ref[k]
        print(f"{k:<14}{base_ref[k]:>10.3f}{ses_best_m[k]:>10.3f}{d:>+10.3f}")

    metrics = {k: v[0] for k, v in results.items()}
    (C.RESULTS_DIR / "ses_metrics.json").write_text(
        json.dumps({"best": best, "features": feats, "metrics": metrics},
                   indent=2), encoding="utf-8")
    np.savez(C.RESULTS_DIR / "oof_ses.npz",
             oof=results[best][1], y=df[C.LABEL_COL].to_numpy(),
             education_low=df["education_low"].to_numpy(), best=best)
    print(f"\n[03] Guardado -> results/ses_metrics.json, oof_ses.npz")
    return 0


if __name__ == "__main__":
    sys.exit(main())
