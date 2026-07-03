# Estadísticas del paciente con Alzheimer/demencia en Latinoamérica

> Deliverable obligatorio del hackathon · Fecha: 2026-07-03
> Objetivo: caracterizar a la población objetivo (quién es, dónde está, qué lo hace vulnerable)
> con datos de repositorios confirmados (OPS/PAHO, 10/66 Dementia Research Group, revisiones
> sistemáticas, CEPAL), para orientar el diseño de la solución (offline-first, voz, smartwatch).
> Todas las cifras están citadas. Ninguna es inventada.

---

## 1. Resumen ejecutivo (lo que manda el diseño)

- **Prevalencia ~8–11% en mayores de 60**; se **triplica cada década de edad** (2.5% → 9.4% → 28.9%).
- **Más mujeres que hombres** (8.97% vs 7.26%) y **más en zona rural** que urbana (8.68% vs 7.71%).
- **Sin educación formal: 21.4%** — más del **doble** que con algo de educación (9.9%). El adulto
  mayor latinoamericano típico con demencia es de **baja escolaridad / analfabeto**.
- **Brecha digital brutal:** solo **23% de hogares rurales** conectados (vs 67% urbanos); adultos
  mayores rurales con **29% menos** probabilidad de acceso a internet.
- **81.6% de los pacientes con demencia son hipertensos** (vs 31.9% sin demencia); la hipertensión
  es el factor de riesgo #1 en LATAM (PAF 18%, el más alto del mundo).
- **54% de la demencia en LATAM es potencialmente prevenible** por factores modificables.

**Traducción a diseño:** offline-first/edge (poca conectividad rural), comunicación **por voz**
(analfabetismo), foco en **mujeres y ≥80 años**, personalización por **baja escolaridad**, y
monitoreo fisiológico **no cognitivo** legítimo vía **hipertensión** (smartwatch PPG).

---

## 2. Magnitud y proyección

| Indicador | Valor | Fuente |
|---|---|---|
| Prevalencia estandarizada por edad (60+) | **8%** (IC 5–11.5%) | PAHO / meta-análisis [1][2] |
| Prevalencia agrupada (pooled) | **10.66%** (IC 9.08–12.34%) | Rev. sistemática 15 países [2] |
| Personas con demencia en LATAM (2013) | **7.8 millones** | [1] |
| Proyección 2030 | **7.6 millones** (desde 3.4M en 2010) | [1] |
| Proyección 2050 | **>27 millones** (~3.5×) | [1] |

La transición demográfica de LATAM es de las más rápidas del mundo: la carga se dispara justo
donde los sistemas de salud son más frágiles.

---

## 3. Distribución por sexo

| Sexo | Prevalencia | Fuente |
|---|---|---|
| **Mujeres** | **8.97%** (IC 7.47–10.60%) | [2] |
| **Hombres** | **7.26%** (IC 5.84–8.80%) | [2] |

Diferencia estadísticamente significativa (p < 0.001). La mayoría de pacientes —y también de
cuidadoras informales— son **mujeres**. La solución debe hablarle bien a ellas.

---

## 4. Distribución por edad

| Grupo etario | Prevalencia | Fuente |
|---|---|---|
| 60–69 | **~2.5%** (IC 0.08–4.0%) | [1] |
| 70–79 | **~9.4%** (IC 5.4–13.2%) | [1] |
| **≥80** | **~28.9%** (IC 20.3–37.2%) | [1] |

Rango por estudio aún más amplio (80+: 16.7%–59.1%) [2]. **El grueso de la carga está en ≥80**,
edad de máxima fragilidad, dependencia y riesgo de desorientación. La franja objetivo del producto
es **adulto mayor de 75+**.

---

## 5. Severidad (leve / moderado / severo)

No hay una distribución por severidad **específica de LATAM** consolidada en la literatura pública.
Como referencia poblacional (Framingham, EE.UU.): **50.4% leve, 30.3% moderado, 19.3% severo** [5].

⚠️ **Matiz crítico para LATAM:** por acceso tardío a especialistas, en la región **se diagnostica
más tarde y en etapas más avanzadas** que en países de altos ingresos [8]. Es decir, la
distribución real latinoamericana está probablemente **corrida hacia moderado/severo** al momento
del diagnóstico. **Implicación:** el diseño debe funcionar también para deterioro moderado
(interfaz ultra-simple, solo voz, iniciativa de la IA), no solo para etapas incipientes.

---

## 6. Rural vs urbano + brecha digital (la razón del offline-first)

| Dimensión | Rural | Urbano | Fuente |
|---|---|---|---|
| Prevalencia de demencia | **8.68%** | 7.71% | [2] |
| Hogares con conexión a internet | **23%** | 67% | CEPAL [6] |
| Banda ancha (promedio LATAM) | — | **45.5%** de hogares | CEPAL [6] |
| Acceso a internet en adultos mayores rurales | **29% menos** probabilidad vs urbano | [7] |

Además, los adultos mayores rurales perciben la tecnología como *"muy complicada"*, *"difícil de
aprender"* [7]. **Conclusión de diseño:** una tecnología dependiente de la nube **excluye** a la
población de mayor prevalencia. El núcleo del paciente **debe correr offline / en el borde** y ser
de fricción casi nula.

---

## 7. Educación / analfabetismo (la razón del voz-primero)

| Nivel educativo | Prevalencia de demencia | Fuente |
|---|---|---|
| **Sin educación formal** | **21.37%** (IC 14.22–29.51%) | [2] |
| Con ≥1 año de educación | 9.88% (IC 7.50–12.54%) | [2] |

La población de estudio en LATAM es predominantemente *"analfabeta o con hasta 4 años de
escolaridad"* [2]. La baja escolaridad explica buena parte del exceso de prevalencia (menor reserva
cognitiva + peor control de factores cardiovasculares + acceso limitado a salud primaria) [2].

**Implicación de diseño:** el paciente **no puede depender de leer/escribir**. La interfaz del
paciente es **conversación por voz**, con un avatar cálido; el texto queda para las apps del equipo
de cuidado (cuidador/médico), que sí son alfabetizados.

---

## 8. Comorbilidad clave: hipertensión (la razón del smartwatch)

| Dato | Valor | Fuente |
|---|---|---|
| Pacientes con demencia que son hipertensos | **81.6%** (vs 31.9% sin demencia) | [3] |
| PAF de hipertensión para demencia en LAC | **18.0%** (el más alto del mundo; global 15.8%) | [4] |
| Prevalencia de hipertensión en adultos mayores (urbano) | 52.6–79.8% | 10/66 [3] |
| Prevalencia de hipertensión en adultos mayores (rural) | 42.6–56.9% | 10/66 [3] |
| Demencia potencialmente prevenible (12 factores modificables) | **54%** LATAM (Chile 62%, Argentina 60%, Bolivia/México 56%, Honduras 54%, Brasil 48%, Perú 45%) | [9] |

**Esto habilita el hardware sin romper la prohibición.** No medimos deterioro cognitivo. Medimos
**parámetros cardiovasculares** (FC, variabilidad, estimación no invasiva de presión por PPG) —
clínicamente pertinentes porque **~8 de cada 10 pacientes son hipertensos** y la hipertensión es el
principal factor modificable. Monitoreo legítimo, orquestado por la arquitectura, reportado a
médico y cuidador.

---

## 9. Perfil sintético del paciente objetivo (para diseño y pitch)

> **Mujer, 78 años, zona rural o periurbana, escolaridad primaria incompleta o analfabeta,
> hipertensa, con conectividad a internet intermitente o nula, que tiende a desorientarse cuando
> sale, cuidada por una hija/familiar mujer que carga sola la mayor parte del cuidado.**

Cada rasgo tiene respaldo estadístico arriba y mapea a una decisión de producto (sección 10).

---

## 10. Implicaciones de diseño (dato → decisión)

| Hallazgo estadístico | Decisión de producto |
|---|---|
| Rural 23% conectividad; +prevalencia rural | **Offline-first / edge LLM**; la nube es opcional (reportes) |
| 21.4% prevalencia en sin-educación; analfabetismo alto | **Interfaz del paciente solo por voz** + avatar expresivo |
| ≥80 concentra la carga; diagnóstico tardío/moderado | UI ultra-simple; **IA con iniciativa** (no espera que el paciente sepa usarla) |
| Mayoría mujeres (pacientes y cuidadoras) | Tono, ejemplos y flujos pensados para ellas |
| 81.6% hipertensos; HTA = factor #1 | **Smartwatch con PPG** (FC/variabilidad, presión estimada) — no cognitivo, permitido |
| Desorientación al salir (entrevista + fragilidad ≥80) | **Ubicación** (AirTag larga duración en pulsera + compartir desde la app) |
| Cuidador carga ~50% del cuidado, solo | **App del equipo** con notificaciones de adherencia/actividad, para aliviar carga |
| 54% prevenible por factores modificables | Acompañamiento (actividad, ánimo, adherencia) tiene base de salud pública |

---

## 11. Fuentes

1. PAHO/WHO — Dementia; y "Dementia in Latin America: Epidemiological Evidence and Implications for Public Policy" (Frontiers Aging Neurosci. 2017). https://www.paho.org/en/topics/dementia · https://pmc.ncbi.nlm.nih.gov/articles/PMC5508025/
2. Ribeiro et al. — "Prevalence of dementia in Latin America and Caribbean countries: systematic review and meta-analyses exploring age, sex, rurality, and education" (31 estudios, 15 países, 96,396 sujetos). https://pmc.ncbi.nlm.nih.gov/articles/PMC9582196/
3. 10/66 Dementia Research Group — "Hypertension prevalence, awareness, treatment and control among older people in Latin America, India and China" (PubMed 22134385). https://pubmed.ncbi.nlm.nih.gov/22134385/
4. "Population attributable fraction of hypertension for dementia: global, regional, and national estimates for 186 countries" (eClinicalMedicine 2023). https://www.thelancet.com/journals/eclinm/article/PIIS2589-5370(23)00189-X/fulltext
5. "Severity Distribution of Alzheimer's Disease Dementia and MCI in the Framingham Heart Study" (referencia poblacional EE.UU.). https://pubmed.ncbi.nlm.nih.gov/33361590/
6. CEPAL — "Older adults in the digital age in Latin America: bridging the digital age divide". https://www.cepal.org/en/publications/44722-older-adults-digital-age-latin-america-bridging-digital-age-divide
7. "Rural and Non-Rural Digital Divide Persists in Older Adults: Internet Access, Usage, and Perception". https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7741499/
8. "A task force for diagnosis and treatment of people with Alzheimer's disease in Latin America" (Frontiers Neurol. 2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC10367107/
9. "Population Attributable Fractions for Risk Factors for Dementia in Latin America" (Lancet Global Health 2024 / PMC11715158). https://pmc.ncbi.nlm.nih.gov/articles/PMC11715158/ · https://www.thelancet.com/journals/langlo/article/PIIS2214-109X(24)00275-4/fulltext

> Nota: cifras de prevalencia por severidad específicas de LATAM no están consolidadas
> públicamente; se usó Framingham como referencia con el matiz de diagnóstico tardío regional.
> Para el pitch, priorizar las cifras de secciones 1, 6, 7 y 8 (las más accionables).
