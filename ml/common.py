"""
common.py — Contrato de features, simulación SES y modelo generativo sintético.

Fuente única de verdad para:
  - Nombres/orden de las features (contrato con backend/biomarkers/extract.py).
  - Simulación documentada de metadata socioeconómica (SES).
  - Generador sintético de features (fallback offline + demo de concepto del
    mecanismo de reserva cognitiva).

Todo el pipeline (00..05) importa de aquí para que el schema sea consistente.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

# Consola Windows (cp1252) crashea con caracteres no-ASCII; forzar UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# --------------------------------------------------------------------------- #
# Rutas
# --------------------------------------------------------------------------- #
ML_DIR = Path(__file__).resolve().parent
DATA_DIR = ML_DIR / "data"
RESULTS_DIR = ML_DIR / "results"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42

# --------------------------------------------------------------------------- #
# Contrato de features (ORDEN IMPORTA — backend debe producir esto)
# --------------------------------------------------------------------------- #
# Léxicas / sintácticas (spaCy es_core_news_lg sobre el transcript)
LEXICAL_FEATURES = [
    "ttr",                 # type-token ratio
    "mattr",               # moving-average TTR (ventana 30)
    "brunet_index",        # W = N^(V^-0.165); bajo => mayor riqueza
    "honore_statistic",    # R = 100*logN / (1 - V1/V); bajo => menor riqueza
    "mean_sentence_length",
    "subordination_density",  # SCONJ por oración
    "noun_ratio",
    "verb_ratio",
    "adj_ratio",
    "pronoun_ratio",
    "content_function_ratio",  # (NOUN+VERB+ADJ+ADV)/(DET+ADP+PRON+CCONJ+SCONJ)
    "n_tokens",
]
# Semánticas (coherencia + perseveración)
SEMANTIC_FEATURES = [
    "coherence_mean",      # coseno medio entre oraciones consecutivas
    "coherence_min",
    "repeated_bigram_ratio",   # perseveración
    "repeated_trigram_ratio",
]
# Temporales / de TIMING (VAD sobre audio, o proxy de disfluencias del transcript).
# Evidencia: transfieren cross-lingual (AUC~0.75 inglés->español zero-shot) y son
# robustas a escolaridad -> se priorizan por robustez/fairness.
TIMING_FEATURES = ["n_pauses", "mean_pause_dur", "silence_ratio", "speech_rate"]

# Acústicas puras (solo si hay audio). Se añaden dinámicamente al schema.
ACOUSTIC_FEATURES = (
    [f"mfcc{i}_mean" for i in range(1, 14)]
    + [f"mfcc{i}_std" for i in range(1, 14)]
    + ["f0_mean", "f0_std", "jitter", "shimmer", "hnr"]
)

# Features del habla usadas por el BASELINE P(AD|Voz).
# (Timing/acústicas se concatenan solo si están disponibles; ver speech_feature_names()).
SPEECH_TEXT_FEATURES = LEXICAL_FEATURES + SEMANTIC_FEATURES

# Covariables SES añadidas por el modelo P(AD|Voz, SES).
# Variables alineadas con fuentes Perú (ENDES/INEI, IDH distrital PNUD).
SES_FEATURES = [
    "education_years",        # años de escolaridad del paciente
    "education_low",          # binaria: 1 si escolaridad baja (<= umbral)
    "parent_education_years", # proxy de reserva intergeneracional
    "occupation_skill",       # skill ocupacional 0(no calif.)-3(profesional)
    "welfare_quintile",       # quintil de bienestar 1-5 (estilo ENDES)
    "urban",                  # binaria: 1 urbano, 0 rural
    "idh",                    # IDH distrital [0,1] (estilo PNUD)
    "native_spanish",         # binaria: 1 español L1, 0 lengua indígena L1
    "bilingual",              # binaria: 1 bilingüe
]

LABEL_COL = "label"          # 0 = HC (control), 1 = AD/MCI (deterioro)
GROUP_COL = "education_low"   # variable de estratificación de fairness


def speech_feature_names(columns) -> list[str]:
    """Features de habla presentes en el dataframe (texto + acústicas si hay)."""
    cols = set(columns)
    feats = [c for c in SPEECH_TEXT_FEATURES if c in cols]
    feats += [c for c in TIMING_FEATURES if c in cols]
    feats += [c for c in ACOUSTIC_FEATURES if c in cols]
    return feats


def ses_feature_names(columns) -> list[str]:
    cols = set(columns)
    return [c for c in SES_FEATURES if c in cols]


# --------------------------------------------------------------------------- #
# Manifest (procedencia del dataset)
# --------------------------------------------------------------------------- #
MANIFEST_PATH = DATA_DIR / "manifest.json"


def write_manifest(d: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def read_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


# --------------------------------------------------------------------------- #
# Simulación SES  (DOCUMENTADA — no es data real salvo Ivanova/TalkBank)
# --------------------------------------------------------------------------- #
EDUCATION_LOW_THRESHOLD = 8  # años; <= 8 => escolaridad baja (primaria/incompleta)


def simulate_ses(labels: np.ndarray, rng: np.random.Generator,
                 confound: bool = False) -> dict:
    """
    Genera metadata SES *sintética* correlacionada de forma DÉBIL-MODERADA con la
    clase, imitando la realidad (baja escolaridad algo más frecuente en positivos
    por sesgo de muestreo, no por causalidad directa).

    Parámetros
    ----------
    confound : si True, además devuelve `reserve_confound`, un desplazamiento
        latente que degrada las features léxicas de sujetos SANOS de baja
        escolaridad (mecanismo de reserva cognitiva). Se usa SOLO en el modo
        sintético para demostrar el concepto; NUNCA se aplica a features reales.

    Devuelve dict de arrays alineados con `labels`.
    """
    n = len(labels)
    # Años de escolaridad: base ~ Normal, empujada abajo débilmente para positivos.
    # En modo confound (demo de concepto) la correlación etiqueta-escolaridad se
    # hace CASI NULA a propósito: así SES aporta SOLO la señal de reserva (permite
    # descontar el confound) y no un atajo "baja escolaridad => AD" que el árbol
    # explotaría subiendo los FP. En modo real se deja la correlación débil realista.
    base = rng.normal(9.5, 3.5, n)
    shift_pos = -0.3 if confound else -1.3
    shift = np.where(labels == 1, shift_pos, 0.0)
    education_years = np.clip(base + shift + rng.normal(0, 1.0, n), 0, 20)
    education_low = (education_years <= EDUCATION_LOW_THRESHOLD).astype(int)

    # Zona: baja escolaridad algo más rural.
    p_urban = np.clip(0.75 - 0.25 * education_low, 0.1, 0.95)
    urban = (rng.random(n) < p_urban).astype(int)

    # IDH local: correlacionado con urbanidad y escolaridad.
    idh = np.clip(0.55 + 0.12 * urban + 0.010 * (education_years - 9.5)
                  + rng.normal(0, 0.05, n), 0.25, 0.95)

    # Lengua materna: indígena más probable en baja escolaridad / rural.
    p_spanish = np.clip(0.92 - 0.22 * education_low - 0.10 * (1 - urban), 0.4, 0.99)
    native_spanish = (rng.random(n) < p_spanish).astype(int)
    # Bilingüismo: más frecuente si L1 no es español.
    p_bil = np.clip(0.25 + 0.45 * (1 - native_spanish) + 0.10 * urban, 0.05, 0.95)
    bilingual = (rng.random(n) < p_bil).astype(int)

    # Escolaridad de los padres: correlacionada con la del paciente (reserva
    # intergeneracional).
    parent_education_years = np.clip(
        0.6 * education_years + rng.normal(3.0, 2.5, n), 0, 20)

    # Skill ocupacional 0-3, sube con escolaridad.
    occ_lin = -1.5 + 0.30 * education_years + rng.normal(0, 1.0, n)
    occupation_skill = np.clip(np.round(occ_lin / 2.0), 0, 3).astype(int)

    # Quintil de bienestar 1-5 (estilo ENDES), correlacionado con IDH/urbano.
    q_lin = 5 * (idh - 0.25) / 0.70 + 0.5 * urban + rng.normal(0, 0.6, n)
    welfare_quintile = np.clip(np.round(q_lin), 1, 5).astype(int)

    out = {
        "education_years": education_years,
        "education_low": education_low,
        "parent_education_years": parent_education_years,
        "occupation_skill": occupation_skill,
        "welfare_quintile": welfare_quintile,
        "urban": urban,
        "idh": idh,
        "native_spanish": native_spanish,
        "bilingual": bilingual,
    }
    if confound:
        # Reserva cognitiva: en SANOS de baja escolaridad, el habla luce
        # empobrecida (menor riqueza léxica/sintáctica) sin patología. Esto es
        # lo que produce FALSOS POSITIVOS en el baseline y lo que la covariable
        # SES permite corregir. Magnitud moderada.
        reserve = np.where((labels == 0) & (education_low == 1),
                           rng.normal(0.9, 0.25, n), 0.0)
        # una fracción de sanos de alta escolaridad no recibe penalización (ruido)
        out["reserve_confound"] = np.clip(reserve, 0, None)
    return out


# --------------------------------------------------------------------------- #
# Generador sintético de features de habla (fallback offline + demo de concepto)
# --------------------------------------------------------------------------- #
def synthesize_feature_matrix(n_per_class: int = 180,
                              rng: np.random.Generator | None = None) -> "pd.DataFrame":
    """
    Genera una matriz de features léxicas/sintácticas/semánticas + SES etiquetada,
    a partir de un modelo generativo DOCUMENTADO. Se usa cuando MultiConAD no está
    disponible (offline) y como demostración del mecanismo de reserva cognitiva.

    Todo aquí es SINTÉTICO. El delta +SES observado sobre esta data es una prueba
    de concepto del mecanismo, no una medición sobre habla real.
    """
    import pandas as pd
    if rng is None:
        rng = np.random.default_rng(RANDOM_STATE)

    n = 2 * n_per_class
    labels = np.array([0] * n_per_class + [1] * n_per_class)
    ses = simulate_ses(labels, rng, confound=True)
    reserve = ses.pop("reserve_confound")

    ad = labels.astype(float)

    # --- Modelo de SEVERIDAD latente (mantiene el AUC en rango realista) ---
    # Léxico/semántico: sesgado por la reserva -> baja escolaridad SANA "parece"
    #   deterioro (fuente de falsos positivos del baseline).
    # Timing: NO depende de reserva -> señal "justa", robusta a escolaridad.
    z_common = rng.normal(0, 1, n)            # estilo/variabilidad individual
    z_tim = rng.normal(0, 1, n)
    # reserva DOMINA el léxico: baja escolaridad sana luce tan empobrecida como AD
    # -> el baseline (que se apoya en léxico) la sobre-diagnostica (FP).
    # timing = señal JUSTA moderada (sin reserva); importante pero no rescata sola.
    sev_lex = 1.0 * ad + 1.6 * reserve + z_common
    sev_tim = 0.9 * ad + z_tim
    sev_lex = (sev_lex - sev_lex.mean()) / sev_lex.std()
    sev_tim = (sev_tim - sev_tim.mean()) / sev_tim.std()

    def flex(base, span, noise):   # léxico/semántico: mayor sev = más deterioro
        return base + span * sev_lex + rng.normal(0, noise, n)

    def ftim(base, span, noise):   # timing
        return base + span * sev_tim + rng.normal(0, noise, n)

    df = pd.DataFrame({
        # léxicas — deterioro baja riqueza léxica
        "ttr":                    np.clip(flex(0.55, -0.07, 0.05), 0.1, 0.95),
        "mattr":                  np.clip(flex(0.63, -0.06, 0.05), 0.1, 0.95),
        "brunet_index":           np.clip(flex(13.0, +1.6, 1.3), 5, 25),
        "honore_statistic":       np.clip(flex(1150, -180, 130), 200, 2200),
        "mean_sentence_length":   np.clip(flex(10.5, -2.2, 2.0), 2, 30),
        "subordination_density":  np.clip(flex(0.45, -0.13, 0.12), 0, 2),
        "noun_ratio":             np.clip(flex(0.21, -0.022, 0.03), 0.02, 0.5),
        "verb_ratio":             np.clip(flex(0.18, +0.015, 0.03), 0.02, 0.5),
        "adj_ratio":              np.clip(flex(0.065, -0.013, 0.02), 0.0, 0.3),
        "pronoun_ratio":          np.clip(flex(0.11, +0.028, 0.03), 0.0, 0.4),
        "content_function_ratio": np.clip(flex(1.05, -0.16, 0.16), 0.2, 3),
        "n_tokens":               np.clip(flex(82, -16, 16), 10, 300),
        # semánticas
        "coherence_mean":         np.clip(flex(0.52, -0.08, 0.07), 0.05, 0.95),
        "coherence_min":          np.clip(flex(0.26, -0.07, 0.07), 0.0, 0.9),
        "repeated_bigram_ratio":  np.clip(flex(0.07, +0.04, 0.03), 0, 0.5),
        "repeated_trigram_ratio": np.clip(flex(0.03, +0.028, 0.02), 0, 0.4),
        # timing — señal fuerte y JUSTA (sin reserva)
        "n_pauses":               np.clip(ftim(9.0, +3.2, 2.2), 0, 40),
        "mean_pause_dur":         np.clip(ftim(0.60, +0.22, 0.14), 0.05, 3),
        "silence_ratio":          np.clip(ftim(0.37, +0.11, 0.07), 0.02, 0.9),
        "speech_rate":            np.clip(ftim(2.9, -0.75, 0.5), 0.3, 7),
    })
    for k, v in ses.items():
        df[k] = v
    df[LABEL_COL] = labels
    return df.sample(frac=1.0, random_state=RANDOM_STATE).reset_index(drop=True)
