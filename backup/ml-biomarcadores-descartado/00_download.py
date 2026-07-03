"""
00_download.py — Descarga MultiConAD (HuggingFace), filtra español, EDA básico.

Estrategia:
  1. Intenta cargar MultiConAD desde una lista de IDs candidatos de HF
     (override con env MULTICONAD_ID). Detecta de forma adaptativa las columnas
     de texto / etiqueta / idioma y filtra el subconjunto español.
  2. Adjunta metadata SES SINTÉTICA (documentada) alineada con la clase.
  3. Si no hay acceso (offline / dataset gated), genera un fallback SINTÉTICO
     de features (ver common.synthesize_feature_matrix) para que el pipeline
     corra end-to-end. Queda marcado en manifest.json (is_synthetic=true).

Salidas:
  ml/data/raw.parquet      (texto+label+SES  ó  features+SES si sintético)
  ml/data/manifest.json    (procedencia y flags)
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

import common as C

CANDIDATE_IDS = [
    os.environ.get("MULTICONAD_ID", "").strip(),
    "aixplain/MultiConAD",
    "MultiConAD/MultiConAD",
    "HemanthSai7/MultiConAD",
]
SPANISH_TOKENS = {"es", "spa", "spanish", "español", "espanol"}
AD_TOKENS = {"ad", "mci", "dementia", "alzheimer", "patient", "cognitive", "impair"}
HC_TOKENS = {"hc", "control", "healthy", "cn", "cognitively normal", "no"}


def _find_col(cols, *needles):
    for c in cols:
        lc = c.lower()
        if any(n in lc for n in needles):
            return c
    return None


def _map_label(v) -> int | None:
    s = str(v).strip().lower()
    if s in {"1", "0"}:
        return int(s)
    if any(t in s for t in HC_TOKENS):
        return 0
    if any(t in s for t in AD_TOKENS):
        return 1
    return None


def try_load_multiconad() -> pd.DataFrame | None:
    try:
        from datasets import get_dataset_config_names, load_dataset
    except Exception as e:  # pragma: no cover
        print(f"[00] `datasets` no disponible ({e}).")
        return None

    for ds_id in [d for d in CANDIDATE_IDS if d]:
        try:
            print(f"[00] Intentando HuggingFace dataset: {ds_id}")
            try:
                configs = get_dataset_config_names(ds_id)
            except Exception:
                configs = [None]
            # Preferir config que mencione español si existe
            es_cfg = next((c for c in configs if c and any(t in c.lower()
                          for t in SPANISH_TOKENS)), None)
            cfg = es_cfg or (configs[0] if configs else None)
            ds = load_dataset(ds_id, cfg) if cfg else load_dataset(ds_id)
            split = "train" if "train" in ds else list(ds.keys())[0]
            df = ds[split].to_pandas()
            print(f"[00] Cargado {ds_id} (config={cfg}, split={split}) "
                  f"shape={df.shape}\n      columnas={list(df.columns)}")

            lang_col = _find_col(df.columns, "lang", "idiom", "language")
            if lang_col:
                mask = df[lang_col].astype(str).str.lower().apply(
                    lambda v: any(t in v for t in SPANISH_TOKENS))
                if mask.any():
                    df = df[mask].copy()
                    print(f"[00] Filtrado español por '{lang_col}': {len(df)} filas")

            text_col = _find_col(df.columns, "transcript", "text", "utter",
                                 "sentence", "content")
            label_col = _find_col(df.columns, "label", "diagnos", "class",
                                  "group", "dx", "target")
            if not text_col or not label_col:
                print(f"[00] No hallé columnas texto/label en {ds_id}; siguiente.")
                continue

            out = pd.DataFrame({
                "id": np.arange(len(df)),
                "text": df[text_col].astype(str).values,
                C.LABEL_COL: [_map_label(v) for v in df[label_col].values],
            })
            out = out.dropna(subset=[C.LABEL_COL])
            out[C.LABEL_COL] = out[C.LABEL_COL].astype(int)
            out = out[out["text"].str.len() > 3].reset_index(drop=True)
            if out[C.LABEL_COL].nunique() < 2 or len(out) < 30:
                print(f"[00] {ds_id}: muy pocas clases/filas útiles ({len(out)}).")
                continue
            return out
        except Exception as e:
            print(f"[00] Falló {ds_id}: {type(e).__name__}: {e}")
    return None


def main():
    rng = np.random.default_rng(C.RANDOM_STATE)
    df = try_load_multiconad()

    if df is not None:
        # Data real (texto). SES sintético SIN confound (reporte honesto).
        ses = C.simulate_ses(df[C.LABEL_COL].to_numpy(), rng, confound=False)
        for k, v in ses.items():
            df[k] = v
        manifest = {
            "dataset": "MultiConAD (HuggingFace)",
            "modality": "text",
            "is_synthetic_features": False,
            "ses_synthetic": True,
            "ses_confound_injected": False,
            "n_samples": int(len(df)),
            "n_positive": int(df[C.LABEL_COL].sum()),
            "n_negative": int((df[C.LABEL_COL] == 0).sum()),
        }
        print("[00] Usando MultiConAD real (texto) + SES sintético (sin confound).")
    else:
        # Fallback: matriz de features sintética con confound de reserva cognitiva.
        df = C.synthesize_feature_matrix(n_per_class=180, rng=rng)
        manifest = {
            "dataset": "SINTÉTICO (fallback offline / demo de concepto)",
            "modality": "features",
            "is_synthetic_features": True,
            "ses_synthetic": True,
            "ses_confound_injected": True,
            "n_samples": int(len(df)),
            "n_positive": int(df[C.LABEL_COL].sum()),
            "n_negative": int((df[C.LABEL_COL] == 0).sum()),
        }
        print("[00] MultiConAD no disponible -> dataset SINTÉTICO (documentado).")

    out_path = C.DATA_DIR / "raw.parquet"
    df.to_parquet(out_path, index=False)
    C.write_manifest(manifest)

    # EDA básico
    print("\n===== EDA =====")
    print(f"Filas: {len(df)}   Positivos(AD/MCI): {manifest['n_positive']}   "
          f"Negativos(HC): {manifest['n_negative']}")
    if "text" in df.columns:
        lens = df["text"].str.split().apply(len)
        print(f"Longitud transcript (tokens): media={lens.mean():.1f} "
              f"min={lens.min()} max={lens.max()}")
    print("Distribución escolaridad baja (education_low):")
    print(df.groupby(C.LABEL_COL)["education_low"].mean().round(3).to_string())
    print(f"\n[00] Guardado -> {out_path}")
    print(f"[00] Manifest -> {C.MANIFEST_PATH}")


if __name__ == "__main__":
    sys.exit(main())
