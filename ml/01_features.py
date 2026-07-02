"""
01_features.py — Extrae features de cada muestra -> ml/data/features.parquet

Dos caminos, según raw.parquet (ver manifest.json):
  A) raw trae `text`  -> extrae:
       léxicas/sintácticas (spaCy es_core_news_lg->sm->blank),
       semánticas (coherencia coseno + perseveración),
       timing PROXY (marcadores de disfluencia/pausa del transcript CHAT),
       acústicas (si hay columna de audio Y librosa/parselmouth/webrtcvad).
  B) raw ya trae columnas de features (modo sintético) -> passthrough validado.

Salida: ml/data/features.parquet  con features + columnas SES + label.
"""
from __future__ import annotations

import re
import sys

import numpy as np
import pandas as pd

import common as C

# --------------------------------------------------------------------------- #
# spaCy (carga perezosa con fallbacks)
# --------------------------------------------------------------------------- #
_NLP = None


def get_nlp():
    global _NLP
    if _NLP is not None:
        return _NLP
    import spacy
    for name in ("es_core_news_lg", "es_core_news_md", "es_core_news_sm"):
        try:
            _NLP = spacy.load(name)
            print(f"[01] spaCy modelo: {name}")
            return _NLP
        except Exception:
            continue
    # Fallback mínimo: sin POS (ratios saldrán 0), pero con sentencizer.
    _NLP = spacy.blank("es")
    _NLP.add_pipe("sentencizer")
    print("[01] AVISO: sin modelo es_core_news_*; ratios POS no disponibles.")
    return _NLP


# --------------------------------------------------------------------------- #
# Features léxicas / sintácticas
# --------------------------------------------------------------------------- #
def lexical_syntactic(doc) -> dict:
    toks = [t for t in doc if t.is_alpha]
    words = [t.text.lower() for t in toks]
    N = len(words)
    if N == 0:
        return {k: 0.0 for k in C.LEXICAL_FEATURES}
    V = len(set(words))
    freq = pd.Series(words).value_counts()
    V1 = int((freq == 1).sum())  # hapax legomena

    ttr = V / N
    # MATTR ventana 30
    w = 30
    if N >= w:
        ratios = [len(set(words[i:i + w])) / w for i in range(0, N - w + 1)]
        mattr = float(np.mean(ratios))
    else:
        mattr = ttr
    brunet = N ** (V ** -0.165) if V > 1 else 0.0
    honore = (100 * np.log(max(N, 2))) / (1 - min(V1 / V, 0.999)) if V > 0 else 0.0

    sents = list(doc.sents) or [doc]
    sent_lens = [len([t for t in s if t.is_alpha]) for s in sents]
    mean_sent_len = float(np.mean(sent_lens)) if sent_lens else 0.0
    n_sconj = sum(1 for t in doc if t.pos_ == "SCONJ")
    subord_density = n_sconj / len(sents) if sents else 0.0

    pos = pd.Series([t.pos_ for t in toks])
    def r(tag):
        return float((pos == tag).mean()) if len(pos) else 0.0
    noun_ratio, verb_ratio, adj_ratio = r("NOUN"), r("VERB"), r("ADJ")
    pron_ratio = r("PRON")
    content = sum((pos == p).sum() for p in ("NOUN", "VERB", "ADJ", "ADV"))
    function = sum((pos == p).sum() for p in ("DET", "ADP", "PRON", "CCONJ", "SCONJ"))
    cf_ratio = content / function if function else float(content)

    return {
        "ttr": ttr, "mattr": mattr, "brunet_index": float(brunet),
        "honore_statistic": float(honore), "mean_sentence_length": mean_sent_len,
        "subordination_density": subord_density, "noun_ratio": noun_ratio,
        "verb_ratio": verb_ratio, "adj_ratio": adj_ratio, "pronoun_ratio": pron_ratio,
        "content_function_ratio": float(cf_ratio), "n_tokens": float(N),
    }


# --------------------------------------------------------------------------- #
# Features semánticas (coherencia + perseveración)
# --------------------------------------------------------------------------- #
def semantic(doc, embedder=None) -> dict:
    sents = [s.text.strip() for s in (doc.sents if doc.has_annotation("SENT_START")
                                      else [doc]) if s.text.strip()]
    # Coherencia entre oraciones consecutivas
    coh = []
    if len(sents) >= 2:
        if embedder is not None:
            vecs = embedder(sents)
        else:
            from sklearn.feature_extraction.text import TfidfVectorizer
            try:
                vecs = TfidfVectorizer().fit_transform(sents).toarray()
            except ValueError:
                vecs = None
        if vecs is not None:
            vecs = np.asarray(vecs, dtype=float)
            norm = np.linalg.norm(vecs, axis=1) + 1e-9
            for i in range(len(sents) - 1):
                c = float(vecs[i] @ vecs[i + 1] / (norm[i] * norm[i + 1]))
                coh.append(c)
    coherence_mean = float(np.mean(coh)) if coh else 0.0
    coherence_min = float(np.min(coh)) if coh else 0.0

    words = [t.text.lower() for t in doc if t.is_alpha]
    def rep_ratio(k):
        if len(words) < k + 1:
            return 0.0
        grams = [tuple(words[i:i + k]) for i in range(len(words) - k + 1)]
        vc = pd.Series(grams).value_counts()
        repeated = int(vc[vc > 1].sum() - (vc > 1).sum())  # repeticiones extra
        return repeated / max(len(grams), 1)
    return {
        "coherence_mean": coherence_mean, "coherence_min": coherence_min,
        "repeated_bigram_ratio": rep_ratio(2), "repeated_trigram_ratio": rep_ratio(3),
    }


# --------------------------------------------------------------------------- #
# Timing PROXY desde marcadores del transcript (CHAT/TalkBank: (.), (..), &-uh)
# --------------------------------------------------------------------------- #
_PAUSE_RE = re.compile(r"\(\.{1,3}\)|#|&[-=]?\w+|\.\.\.|\bumm?\b|\beh+\b|\bmmm?\b",
                       re.IGNORECASE)


def timing_proxy(text: str) -> dict | None:
    if not text:
        return None
    marks = _PAUSE_RE.findall(text)
    n_words = max(len(re.findall(r"\w+", text)), 1)
    if not marks:
        return None  # sin marcadores -> no inventamos timing
    n_pauses = len(marks)
    # duración aproximada: (.)=0.3s (..)=0.6 (...)=1.0 ; filled ~0.4
    dur = 0.0
    for m in marks:
        if m == "(...)" or m == "...":
            dur += 1.0
        elif m == "(..)":
            dur += 0.6
        elif m == "(.)":
            dur += 0.3
        else:
            dur += 0.4
    mean_pause = dur / n_pauses
    est_speech_time = n_words / 3.5  # ~3.5 palabras/s de referencia
    silence_ratio = dur / (dur + est_speech_time)
    speech_rate = n_words / (dur + est_speech_time)
    return {"n_pauses": float(n_pauses), "mean_pause_dur": float(mean_pause),
            "silence_ratio": float(silence_ratio), "speech_rate": float(speech_rate)}


# --------------------------------------------------------------------------- #
# Acústicas (solo si hay audio + libs). Placeholder invocable en Colab.
# --------------------------------------------------------------------------- #
def acoustic_from_path(path: str) -> dict | None:
    try:
        import librosa
        import parselmouth
        from parselmouth.praat import call
    except Exception:
        return None
    try:
        y, sr = librosa.load(path, sr=16000)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        feats = {}
        for i in range(13):
            feats[f"mfcc{i+1}_mean"] = float(mfcc[i].mean())
            feats[f"mfcc{i+1}_std"] = float(mfcc[i].std())
        snd = parselmouth.Sound(path)
        pitch = snd.to_pitch()
        f0 = pitch.selected_array["frequency"]
        f0 = f0[f0 > 0]
        feats["f0_mean"] = float(f0.mean()) if len(f0) else 0.0
        feats["f0_std"] = float(f0.std()) if len(f0) else 0.0
        pp = call(snd, "To PointProcess (periodic, cc)", 75, 500)
        feats["jitter"] = float(call(pp, "Get jitter (local)", 0, 0, 1e-4, 0.02, 1.3))
        feats["shimmer"] = float(call([snd, pp], "Get shimmer (local)",
                                      0, 0, 1e-4, 0.02, 1.3, 1.6))
        harm = snd.to_harmonicity()
        feats["hnr"] = float(harm.values[harm.values != -200].mean())
        return feats
    except Exception as e:
        print(f"[01] acústica falló en {path}: {e}")
        return None


# --------------------------------------------------------------------------- #
def build_embedder():
    """sentence-transformers si está; si no, None (usa TF-IDF)."""
    try:
        from sentence_transformers import SentenceTransformer
        m = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        print("[01] Embeddings: sentence-transformers multilingüe.")
        return lambda sents: m.encode(sents)
    except Exception:
        print("[01] Embeddings: TF-IDF fallback (sentence-transformers no disponible).")
        return None


def main():
    raw = pd.read_parquet(C.DATA_DIR / "raw.parquet")
    manifest = C.read_manifest()

    if manifest.get("is_synthetic_features") or "text" not in raw.columns:
        # Passthrough sintético: ya trae features + SES + label.
        feats = C.speech_feature_names(raw.columns) + C.ses_feature_names(raw.columns)
        out = raw[feats + [C.LABEL_COL]].copy()
        print(f"[01] Passthrough sintético: {out.shape[1]-1} features, {len(out)} filas.")
    else:
        nlp = get_nlp()
        embedder = build_embedder()
        audio_col = next((c for c in raw.columns
                          if "audio" in c.lower() or "path" in c.lower() or "wav" in c.lower()),
                         None)
        rows = []
        for _, r in raw.iterrows():
            text = str(r["text"])
            doc = nlp(text)
            feat = {}
            feat.update(lexical_syntactic(doc))
            feat.update(semantic(doc, embedder))
            tp = timing_proxy(text)
            if tp:
                feat.update(tp)
            if audio_col and isinstance(r.get(audio_col), str):
                ac = acoustic_from_path(r[audio_col])
                if ac:
                    feat.update(ac)
            for s in C.SES_FEATURES:
                if s in r:
                    feat[s] = r[s]
            feat[C.LABEL_COL] = int(r[C.LABEL_COL])
            rows.append(feat)
        out = pd.DataFrame(rows)
        # timing proxy: si NINGUNA fila tuvo marcadores, columnas ausentes (ok).
        present_timing = [c for c in C.TIMING_FEATURES if c in out.columns]
        print(f"[01] Extraídas {out.shape[1]-1} features de {len(out)} transcripts. "
              f"Timing proxy: {'sí ('+','.join(present_timing)+')' if present_timing else 'no (sin marcadores)'}.")

    out = out.fillna(0.0)
    out.to_parquet(C.DATA_DIR / "features.parquet", index=False)
    speech = C.speech_feature_names(out.columns)
    ses = C.ses_feature_names(out.columns)
    print(f"[01] Features de habla ({len(speech)}): {speech}")
    print(f"[01] Covariables SES ({len(ses)}): {ses}")
    print(f"[01] Guardado -> {C.DATA_DIR / 'features.parquet'}")


if __name__ == "__main__":
    sys.exit(main())
