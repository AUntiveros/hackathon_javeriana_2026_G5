# Prompt para terminal paralela — Entrenamiento del modelo de predicción (impacto novedoso)

> Pega TODO el bloque de abajo en una **nueva sesión de Claude Code (Fable)** en otra terminal.
> Corre en paralelo mientras la sesión principal avanza el multiagente + backend.
> Objetivo científico: demostrar que `P(AD|Voz, Contexto SES)` > `P(AD|Voz)` en español, con fairness por escolaridad. **Este es el diferenciador publicable del proyecto.**

---

## PROMPT (copiar desde aquí) ⬇️

```
Eres un ingeniero de ML trabajando en el track de biomarcadores de voz de un proyecto de
detección de Alzheimer en español para una hackathon. Trabaja de forma autónoma y ordenada.

CONTEXTO:
- Hipótesis central: predecir Alzheimer/deterioro cognitivo desde el habla mejora al añadir
  metadata socioeconómica (escolaridad, zona urbana/rural, IDH, lengua materna) como covariable,
  porque esa metadata aproxima la RESERVA COGNITIVA y reduce falsos positivos en poblaciones de
  baja escolaridad. Casi nadie lo ha medido sistemáticamente en español. Ese delta es el impacto.
- Tarea de referencia: descripción de imagen tipo "Cookie Theft" (habla espontánea).
- Todo el pipeline y resultados van a la carpeta ml/ del repo actual.

DATASET:
- Plan A (inmediato, usar YA): MultiConAD en HuggingFace (unifica datasets multilingües incl.
  español, con etiquetas AD/MCI/HC). Descargar con `datasets`. Filtrar subconjunto español.
- Plan B (upgrade si se consigue acceso): Ivanova Corpus vía DementiaBank/TalkBank (361 sujetos
  español, incluye nivel educativo). Requiere membresía — si no hay credenciales, quedarse con Plan A.
- Si el dataset carece de metadata SES real, SIMULAR metadata plausible correlacionada con la clase
  de forma realista (NO trivial: la correlación debe ser débil-moderada, como en la vida real) y
  DOCUMENTAR claramente que es sintética para el experimento de concepto.

PIPELINE A CONSTRUIR (en ml/):
1. ml/00_download.py — descarga MultiConAD, filtra español, guarda a ml/data/. EDA básico
   (conteo por clase, duración, metadata disponible). Imprime resumen.
2. ml/01_features.py — de cada muestra extrae:
   - Acústicas (si hay audio): librosa + praat-parselmouth → MFCC(13) media/std, F0 media/std,
     jitter, shimmer, HNR, tasa de habla.
   - Temporales/pausas: webrtcvad → nº pausas, duración media de pausa, ratio silencio/habla.
   - Léxicas/sintácticas (del transcript, spaCy es_core_news_lg): TTR, MATTR, Brunet, Honoré,
     longitud media de oración, densidad de subordinadas, densidad de sustantivos/verbos.
   - Semánticas simples: repetición/perseveración (n-gramas repetidos), coherencia (similitud
     coseno entre oraciones consecutivas con embeddings).
   Si SOLO hay texto (sin audio), usa features léxicas/sintácticas/semánticas y omite acústicas.
   Guarda tabla ml/data/features.parquet con columna de clase + columnas SES.
3. ml/02_baseline.py — modelo P(AD|Voz): entrena XGBoost, SVM(RBF) y RandomForest SOLO con
   features del habla. CV estratificada 5-fold. Reporta AUC, F1, sensibilidad, especificidad.
4. ml/03_ses_model.py — modelo P(AD|Voz, SES): mismos algoritmos + covariables SES.
   Compara contra baseline. Reporta el DELTA de cada métrica.
5. ml/04_fairness.py — ESTRATIFICA sensibilidad/especificidad por nivel educativo (bajo vs alto).
   Muestra que el baseline tiene MÁS falsos positivos en escolaridad baja y que el modelo +SES
   los reduce. Genera:
   - ml/results/metrics_comparison.csv (baseline vs +SES, todas las métricas)
   - ml/results/fairness_by_education.csv
   - ml/results/*.png (curvas ROC comparadas, barras de FPR por grupo, importancia de features)
6. ml/05_export.py — reentrena el mejor modelo +SES con todo el train, guarda:
   - ml/model.pkl (pipeline sklearn: scaler + modelo)
   - ml/feature_schema.json (orden y nombres de features esperadas por el backend)
   - ml/model_card.md (dataset, features, métricas, límites, nota de metadata sintética si aplica)

REGLAS:
- Escribe requirements en ml/requirements.txt. Usa entorno reproducible.
- Prefiere que corra en Colab (GPU gratis) para Whisper si hay audio; en local para el resto.
- NO inventes métricas: reporta lo que salga. Si el delta +SES es pequeño, dilo y analiza por qué.
- Deja un ml/README.md con cómo reproducir y un resumen de 5 líneas de resultados para el pitch.
- El entregable crítico para el backend es ml/model.pkl + ml/feature_schema.json — que el schema
  coincida con lo que backend/biomarkers/extract.py va a producir (features en el mismo orden).

Empieza descargando el dataset (paso 1) y avanza secuencialmente. Reporta al terminar cada paso.
```

## PROMPT (fin) ⬆️

---

---

## AMPLIACIÓN (pegar como follow-up a la terminal de entrenamiento)

> Refuerzos derivados de la carpeta `revisiones puntuales/`. Mejoran rigor y matchean la evidencia 2026.

```
Refuerzos al pipeline de biomarcadores (aplica sobre lo que ya avanzaste):

1. CLASIFICADOR: prioriza árboles (XGBoost/RandomForest) — evidencia MultiConAD muestra que el
   español rinde mejor con clasificadores de árboles que con modelos densos de texto. Mantén SVM
   solo como referencia.
2. FEATURES: da prioridad a los de TIMING/temporales (nº y duración de pausas, tasa de habla,
   ratio silencio/habla) porque transfieren cross-lingual (AUC ~0.75 inglés→español zero-shot);
   los léxicos NO transfieren bien. Reporta importancia de features y confirma que las temporales
   pesan.
3. METADATA SES (columnas del modelo +SES): años de escolaridad (y de los padres si existe),
   ocupación/skill ocupacional, quintil de bienestar (estilo ENDES), IDH distrital (0-1, estilo
   PNUD Perú), urbano/rural, lengua materna, bilingüe (bool). Si son sintéticas, correlación
   débil-moderada realista y documentado.
4. FAIRNESS (04_fairness.py): añade la métrica Equal Opportunity (igualdad de TPR/sensibilidad
   entre escolaridad baja vs alta) además de FPR por grupo. Prueba Borderline-SMOTE para
   rebalancear el grupo de baja escolaridad. Opcional si hay tiempo: Adversarial Debiasing.
   Objetivo a demostrar: el baseline tiene MENOR sensibilidad y MÁS falsos positivos en
   escolaridad baja; el modelo +SES cierra esa brecha.
5. CONTEXTO/BENCHMARK para el model_card y el pitch (no son metas obligatorias, son referencia):
   Whisper-medium ~0.73 acc / 0.80 AUC en ADReSS; VoxCog 0.875 (usa prior dialectal). Reporta lo
   que TÚ obtengas honestamente y compáralo cualitativamente.
6. NARRATIVA: en ml/README deja 5 líneas con el delta baseline vs +SES y la frase de impacto:
   "un modelo agnóstico al contexto clasifica mal a un adulto mayor quechuahablante de baja
   escolaridad; añadir metadata SES reduce ese falso positivo".
```

---

### Notas para Alvaro
- Este track es independiente: no toca el backend salvo por el contrato `model.pkl` + `feature_schema.json`.
- Coordina UNA cosa entre ambas terminales: **el orden y nombres de las features** (que `extract.py` del backend y `01_features.py` del ML coincidan). Define el `feature_schema.json` primero y compártelo.
- Si el dataset con audio no llega, el modelo texto-only ya demuestra el concepto (léxico+sintáctico+semántico son fuertes en Cookie Theft).
