"""
modeling.py — Modelos y evaluación con CV estratificada 5-fold (compartido por 02..05).

Clasificadores (evidencia MultiConAD: el español rinde mejor con ÁRBOLES):
  - XGBoost         (primario)
  - RandomForest    (primario)
  - SVM (RBF)       (solo REFERENCIA)
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

import common as C

N_SPLITS = 5

# Modelos primarios primero; SVM marcado como referencia.
PRIMARY_MODELS = ["XGBoost", "RandomForest"]
REFERENCE_MODELS = ["SVM_RBF"]


def _xgb():
    from xgboost import XGBClassifier
    return XGBClassifier(
        n_estimators=300, max_depth=4, learning_rate=0.05,
        subsample=0.9, colsample_bytree=0.9, eval_metric="logloss",
        random_state=C.RANDOM_STATE, n_jobs=-1,
    )


def build_models() -> dict:
    """Devuelve pipelines (scaler + clf). Orden: primarios, luego referencia."""
    return {
        "XGBoost": Pipeline([("scaler", StandardScaler()), ("clf", _xgb())]),
        "RandomForest": Pipeline([("scaler", StandardScaler()),
                                  ("clf", RandomForestClassifier(
                                      n_estimators=400, max_depth=None,
                                      min_samples_leaf=2, class_weight="balanced",
                                      random_state=C.RANDOM_STATE, n_jobs=-1))]),
        "SVM_RBF": Pipeline([("scaler", StandardScaler()),
                             ("clf", SVC(kernel="rbf", C=2.0, gamma="scale",
                                         class_weight="balanced", probability=True,
                                         random_state=C.RANDOM_STATE))]),
    }


def metrics_from(y_true, y_prob, thr=0.5) -> dict:
    y_pred = (y_prob >= thr).astype(int)
    tp = int(((y_pred == 1) & (y_true == 1)).sum())
    tn = int(((y_pred == 0) & (y_true == 0)).sum())
    fp = int(((y_pred == 1) & (y_true == 0)).sum())
    fn = int(((y_pred == 0) & (y_true == 1)).sum())
    sens = tp / (tp + fn) if (tp + fn) else 0.0   # TPR / recall+
    spec = tn / (tn + fp) if (tn + fp) else 0.0   # TNR
    try:
        auc = roc_auc_score(y_true, y_prob)
    except ValueError:
        auc = float("nan")
    return {
        "auc": auc, "f1": f1_score(y_true, y_pred, zero_division=0),
        "sensitivity": sens, "specificity": spec,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }


def cv_oof(X, y, model, n_splits=N_SPLITS):
    """CV estratificada -> probabilidades out-of-fold alineadas con y."""
    y = np.asarray(y)
    X = np.asarray(X, dtype=float)
    oof = np.zeros(len(y), dtype=float)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=C.RANDOM_STATE)
    for tr, te in skf.split(X, y):
        from sklearn.base import clone
        m = clone(model)
        m.fit(X[tr], y[tr])
        oof[te] = m.predict_proba(X[te])[:, 1]
    return oof


def evaluate_all(df, feature_cols, label_col=C.LABEL_COL):
    """Corre los 3 modelos, devuelve dict nombre -> (metrics, oof_probs)."""
    X = df[feature_cols].to_numpy(dtype=float)
    y = df[label_col].to_numpy(dtype=int)
    results = {}
    for name, model in build_models().items():
        oof = cv_oof(X, y, model)
        results[name] = (metrics_from(y, oof), oof)
    return results


def best_model_name(results: dict) -> str:
    """Mejor por AUC, restringido a modelos PRIMARIOS (árboles)."""
    cand = {k: v for k, v in results.items() if k in PRIMARY_MODELS}
    cand = cand or results
    return max(cand, key=lambda k: cand[k][0]["auc"])
