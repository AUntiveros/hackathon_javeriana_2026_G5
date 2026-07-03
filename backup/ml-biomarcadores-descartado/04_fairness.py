"""
04_fairness.py — Fairness estratificado por escolaridad (baja vs alta).

Demuestra la hipótesis: el baseline (solo voz) tiene MÁS falsos positivos y MENOR
sensibilidad en escolaridad baja; el modelo +SES cierra la brecha.

Métricas por grupo: sensibilidad (TPR), especificidad, FPR, FNR.
Métricas de equidad: Equal Opportunity gap (|TPR_alta − TPR_baja|), FPR gap.
Extra: Borderline-SMOTE rebalanceando el grupo de baja escolaridad (si imblearn).

Salidas:
  results/metrics_comparison.csv
  results/fairness_by_education.csv
  results/roc_comparison.png, results/fpr_by_education.png, results/feature_importance.png
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

import common as C
import modeling as M


def group_metrics(y, prob, group, thr=0.5):
    """Métricas para group==0 (alta escolaridad) y group==1 (baja)."""
    rows = []
    for g, gname in [(0, "alta"), (1, "baja")]:
        mask = group == g
        if mask.sum() == 0:
            continue
        m = M.metrics_from(y[mask], prob[mask], thr)
        fpr = m["fp"] / (m["fp"] + m["tn"]) if (m["fp"] + m["tn"]) else 0.0
        fnr = m["fn"] / (m["fn"] + m["tp"]) if (m["fn"] + m["tp"]) else 0.0
        rows.append({"group": gname, "n": int(mask.sum()),
                     "sensitivity": m["sensitivity"], "specificity": m["specificity"],
                     "fpr": fpr, "fnr": fnr})
    return pd.DataFrame(rows)


def group_threshold_calibration(y, prob, group, target_fpr=None):
    """
    Post-procesamiento SES-aware: umbral POR GRUPO de escolaridad que iguala el
    FPR entre grupos (componente de Equalized Odds). Es la forma efectiva de usar
    el contexto SES para corregir el sobre-diagnóstico en baja escolaridad, cuando
    añadir SES como covariable cruda no basta.

    Umbral del grupo g = cuantil de las probs de los CONTROLES de g tal que su
    FPR quede en `target_fpr`. Por defecto target = FPR del grupo de alta
    escolaridad con umbral 0.5 (igualar al grupo aventajado).
    """
    if target_fpr is None:
        hc_hi = prob[(group == 0) & (y == 0)]
        target_fpr = float((hc_hi >= 0.5).mean()) if len(hc_hi) else 0.25
    rows = []
    thresholds = {}
    for g, gname in [(0, "alta"), (1, "baja")]:
        m = group == g
        hc = prob[m & (y == 0)]
        t = float(np.quantile(hc, 1 - target_fpr)) if len(hc) else 0.5
        thresholds[gname] = t
        mm = M.metrics_from(y[m], prob[m], thr=t)
        fpr = mm["fp"] / (mm["fp"] + mm["tn"]) if (mm["fp"] + mm["tn"]) else 0.0
        rows.append({"group": gname, "n": int(m.sum()), "threshold": round(t, 3),
                     "sensitivity": mm["sensitivity"], "specificity": mm["specificity"],
                     "fpr": fpr, "fnr": mm["fn"] / (mm["fn"] + mm["tp"]) if (mm["fn"] + mm["tp"]) else 0.0})
    return pd.DataFrame(rows), target_fpr


def smote_fairness(df, feats):
    """CV con Borderline-SMOTE dentro de cada fold de entrenamiento."""
    try:
        from imblearn.over_sampling import BorderlineSMOTE
    except Exception:
        print("[04] imbalanced-learn no disponible; salto Borderline-SMOTE.")
        return None
    from sklearn.base import clone
    from sklearn.model_selection import StratifiedKFold
    X = df[feats].to_numpy(float)
    y = df[C.LABEL_COL].to_numpy(int)
    grp = df["education_low"].to_numpy(int)
    # etiqueta compuesta clase×grupo para rebalancear el subgrupo baja+positivo
    comp = y * 2 + grp
    oof = np.zeros(len(y))
    skf = StratifiedKFold(5, shuffle=True, random_state=C.RANDOM_STATE)
    model = M.build_models()["XGBoost"]
    for tr, te in skf.split(X, y):
        try:
            sm = BorderlineSMOTE(random_state=C.RANDOM_STATE, k_neighbors=3)
            Xr, cr = sm.fit_resample(X[tr], comp[tr])
            yr = (cr >= 2).astype(int)  # recuperar clase de la etiqueta compuesta
        except Exception:
            Xr, yr = X[tr], y[tr]
        m = clone(model); m.fit(Xr, yr)
        oof[te] = m.predict_proba(X[te])[:, 1]
    return group_metrics(y, oof, grp)


def plots(df, feats_ses):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from sklearn.metrics import roc_curve
    except Exception as e:
        print(f"[04] matplotlib no disponible ({e}); salto PNGs.")
        return
    b = np.load(C.RESULTS_DIR / "oof_baseline.npz", allow_pickle=True)
    s = np.load(C.RESULTS_DIR / "oof_ses.npz", allow_pickle=True)
    y = b["y"]

    # ROC comparado
    fig, ax = plt.subplots(figsize=(5, 5))
    for arr, lab in [(b["oof"], "Baseline (voz)"), (s["oof"], "+SES (voz+contexto)")]:
        fpr, tpr, _ = roc_curve(y, arr)
        auc = M.metrics_from(y, arr)["auc"]
        ax.plot(fpr, tpr, label=f"{lab}  AUC={auc:.3f}")
    ax.plot([0, 1], [0, 1], "k--", lw=0.8)
    ax.set_xlabel("FPR"); ax.set_ylabel("TPR (sensibilidad)")
    ax.set_title("ROC: Baseline vs +SES"); ax.legend(loc="lower right")
    fig.tight_layout(); fig.savefig(C.RESULTS_DIR / "roc_comparison.png", dpi=130)
    plt.close(fig)

    # FPR por grupo de escolaridad
    grp = b["education_low"]
    gb = group_metrics(y, b["oof"], grp)
    gs = group_metrics(y, s["oof"], grp)
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(gb)); w = 0.35
    ax.bar(x - w/2, gb["fpr"], w, label="Baseline", color="#d1495b")
    ax.bar(x + w/2, gs["fpr"], w, label="+SES", color="#2a9d8f")
    ax.set_xticks(x); ax.set_xticklabels("escolaridad " + gb["group"])
    ax.set_ylabel("FPR (falsos positivos)")
    ax.set_title("Falsos positivos por escolaridad"); ax.legend()
    fig.tight_layout(); fig.savefig(C.RESULTS_DIR / "fpr_by_education.png", dpi=130)
    plt.close(fig)

    # Importancia de features (mejor modelo +SES, ajustado a toda la data)
    from sklearn.base import clone
    best = str(s["best"])
    model = clone(M.build_models()[best])
    X = df[feats_ses].to_numpy(float); yy = df[C.LABEL_COL].to_numpy(int)
    model.fit(X, yy)
    clf = model.named_steps["clf"]
    imp = getattr(clf, "feature_importances_", None)
    if imp is not None:
        order = np.argsort(imp)[-18:]
        names = np.array(feats_ses)[order]
        colors = ["#e9c46a" if n in C.SES_FEATURES else
                  ("#2a9d8f" if n in C.TIMING_FEATURES else "#264653") for n in names]
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.barh(range(len(names)), imp[order], color=colors)
        ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=8)
        ax.set_title(f"Importancia de features — {best} (+SES)\n"
                     "amarillo=SES  verde=timing  azul=léxico/sem")
        fig.tight_layout(); fig.savefig(C.RESULTS_DIR / "feature_importance.png", dpi=130)
        plt.close(fig)
    print("[04] PNGs -> roc_comparison, fpr_by_education, feature_importance")


def main():
    df = pd.read_parquet(C.DATA_DIR / "features.parquet")
    if "education_low" not in df.columns:
        print("[04] Sin 'education_low'; no se puede estratificar."); return 1
    speech = C.speech_feature_names(df.columns)
    ses = C.ses_feature_names(df.columns)
    feats_ses = speech + ses

    b = np.load(C.RESULTS_DIR / "oof_baseline.npz", allow_pickle=True)
    s = np.load(C.RESULTS_DIR / "oof_ses.npz", allow_pickle=True)
    y, grp = b["y"], b["education_low"]

    gb = group_metrics(y, b["oof"], grp); gb.insert(0, "model", "baseline")
    gs = group_metrics(y, s["oof"], grp); gs.insert(0, "model", "+SES")
    fairness = pd.concat([gb, gs], ignore_index=True)

    print("\n===== FAIRNESS por escolaridad =====")
    print(fairness.round(3).to_string(index=False))

    def eo_gap(g):  # |TPR_alta - TPR_baja|
        d = g.set_index("group")["sensitivity"]
        return abs(d.get("alta", 0) - d.get("baja", 0))
    def fpr_gap(g):
        d = g.set_index("group")["fpr"]
        return abs(d.get("alta", 0) - d.get("baja", 0))

    print("\n===== EQUIDAD =====")
    print(f"Equal Opportunity gap (|ΔTPR|):  baseline={eo_gap(gb):.3f}  +SES={eo_gap(gs):.3f}")
    print(f"FPR gap (|ΔFPR|):                baseline={fpr_gap(gb):.3f}  +SES={fpr_gap(gs):.3f}")
    fp_low_base = gb.set_index("group").loc["baja", "fpr"] if "baja" in gb["group"].values else float("nan")
    fp_low_ses = gs.set_index("group").loc["baja", "fpr"] if "baja" in gs["group"].values else float("nan")
    print(f"FPR en escolaridad BAJA:         baseline={fp_low_base:.3f}  +SES={fp_low_ses:.3f}  "
          f"(Δ={fp_low_ses - fp_low_base:+.3f})")

    # Calibración por grupo (post-procesamiento SES-aware) sobre el modelo +SES
    cal, target = group_threshold_calibration(y, s["oof"], grp)
    cal.insert(0, "model", "+SES+calibrado")
    fairness = pd.concat([fairness, cal], ignore_index=True)
    print(f"\n===== +SES + CALIBRACIÓN por grupo (target FPR={target:.3f}) =====")
    print(cal.round(3).to_string(index=False))
    fp_low_cal = cal.set_index("group").loc["baja", "fpr"] if "baja" in cal["group"].values else float("nan")
    sn_low_base = gb.set_index("group").loc["baja", "sensitivity"]
    sn_low_cal = cal.set_index("group").loc["baja", "sensitivity"]
    print(f"FPR baja escolaridad: baseline={fp_low_base:.3f} -> calibrado={fp_low_cal:.3f}  "
          f"(Δ={fp_low_cal - fp_low_base:+.3f}) | sensibilidad baja: {sn_low_base:.3f} -> {sn_low_cal:.3f}")

    # Borderline-SMOTE
    sm = smote_fairness(df, feats_ses)
    if sm is not None:
        sm.insert(0, "model", "+SES+SMOTE")
        fairness = pd.concat([fairness, sm], ignore_index=True)
        print("\n===== +SES + Borderline-SMOTE (rebalanceo baja escolaridad) =====")
        print(sm.round(3).to_string(index=False))

    fairness.to_csv(C.RESULTS_DIR / "fairness_by_education.csv", index=False)

    # metrics_comparison.csv (global)
    base_m = json.loads((C.RESULTS_DIR / "baseline_metrics.json").read_text(encoding="utf-8"))
    ses_m = json.loads((C.RESULTS_DIR / "ses_metrics.json").read_text(encoding="utf-8"))
    bb, sb = base_m["best"], ses_m["best"]
    rows = []
    for k in ("auc", "f1", "sensitivity", "specificity"):
        bv = base_m["metrics"][bb][k]; sv = ses_m["metrics"][sb][k]
        rows.append({"metric": k, "baseline": round(bv, 4),
                     "ses": round(sv, 4), "delta": round(sv - bv, 4)})
    rows.append({"metric": "equal_opportunity_gap", "baseline": round(eo_gap(gb), 4),
                 "ses": round(eo_gap(gs), 4), "delta": round(eo_gap(gs) - eo_gap(gb), 4)})
    rows.append({"metric": "fpr_gap", "baseline": round(fpr_gap(gb), 4),
                 "ses": round(fpr_gap(gs), 4), "delta": round(fpr_gap(gs) - fpr_gap(gb), 4)})
    comp = pd.DataFrame(rows)
    comp.to_csv(C.RESULTS_DIR / "metrics_comparison.csv", index=False)
    print("\n===== metrics_comparison.csv =====")
    print(comp.to_string(index=False))

    plots(df, feats_ses)
    print("\n[04] CSVs -> metrics_comparison.csv, fairness_by_education.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
