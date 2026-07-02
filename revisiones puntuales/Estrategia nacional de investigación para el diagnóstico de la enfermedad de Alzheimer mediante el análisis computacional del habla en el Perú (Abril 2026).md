# **Informe Estratégico: IA y Análisis del Habla para la Detección de Alzheimer en Población Peruana (Edición 2026\)**

## **1\. Resumen Ejecutivo**

A principios de 2026, el campo de los biomarcadores digitales de voz ha pasado de la experimentación a la validación multilingüe masiva. La aprobación del **Plan Nacional de Alzheimer 2026-2028** en Perú ofrece un marco institucional sin precedentes para la investigación aplicada.1 La oportunidad crítica para un investigador peruano radica en la **Validación Trans-Dialectal**: utilizar los modelos de cimentación (como Whisper o VoxCog) entrenados en datasets globales para demostrar su eficacia —o necesidad de ajuste— en las variantes del español peruano (costeño, andino y amazónico) y en poblaciones bilingües Quechua-Español.3

## ---

**2\. Inventario Global de Datasets de Habla y Alzheimer (Actualizado 2026\)**

El acceso a estos datos es el primer paso para realizar un *benchmarking* robusto antes de recolectar data local.

### **2.1. Datasets en Español (Prioridad para Perú)**

| Dataset | Origen | Composición (Sujetos/Tareas) | Acceso | Papeles Relevantes (2025-2026) |
| :---- | :---- | :---- | :---- | :---- |
| **Ivanova Corpus** (DementiaBank) | España (Salamanca) | 361 sujetos (74 AD, 90 MCI, 197 HC). Tarea: Descripción de imagen "Cookie Theft" y lectura.6 | **Membresía TalkBank**: Requiere correo a talkbank@cmu.edu (estudiantes deben ser registrados por su tutor).8 | Utilizado en el reto **MultiConAD (2025)** para evaluar transferencia translingüística.10 |
| **GITA/Paisa Dataset** | Colombia (Antioquia) | 114 sujetos (incluye portadores de mutación genética "Paisa"). Tarea: Habla espontánea (Cookie Theft). | **Restringido**: Contacto directo con el GITA Lab (U. de Antioquia) mediante convenio de investigación. | Primer estudio enfocado en Alzheimer genético y de inicio temprano. |
| **PerLA Corpus** | España | 21 sujetos (AD). Enfoque en pragmática y lingüística clínica.6 | **Público/Educativo**: Disponible en DementiaBank bajo reglas de uso general.9 | Análisis de la "falla pragmática" y coherencia narrativa.12 |

### **2.2. Datasets en Inglés (Estándares Globales)**

| Dataset | Origen | Sujetos / Contenido | Acceso | Nota Técnica |
| :---- | :---- | :---- | :---- | :---- |
| **Pitt Corpus** | EE.UU. | 497 narraciones (255 AD, 42 MCI, 243 HC). Longitudinal.6 | **TalkBank Membership**: El estándar de oro para entrenamiento de modelos.11 | Contiene grabaciones anuales de los mismos pacientes (1983-1988).7 |
| **Delaware Corpus** | EE.UU. | 53 sujetos (20 HC, 33 MCI). Protocolo expandido de DementiaBank.13 | **TalkBank Membership**: Data reciente (2023-2025).13 | Utilizado en validaciones de modelos LLaMA-8B y GPT-4o fine-tuned (2026).14 |
| **VAS (Voice Assistant)** | Global/Digital | 40 sujetos (65+ años). Comandos de voz a Amazon Alexa. | **Bajo demanda**: Requiere aprobación ética debido a la naturaleza de los comandos diarios.6 | Evalúa la usabilidad de asistentes de voz en pacientes con deterioro cognitivo. |

### **2.3. Datasets Asiáticos e India (Alta Variabilidad Fonética)**

| Dataset | Idioma / Origen | Sujetos / Tareas | Acceso | Relevancia |
| :---- | :---- | :---- | :---- | :---- |
| **NCMMSC / NCMMSE** | Chino (Mandarín) | 280 sujetos (79 AD, 93 MCI, 108 HC). Tareas de fluidez y descripción.6 | **Restringido/Challenge**: Originalmente lanzado para el reto NCMMSC.10 | Crucial para probar la robustez de modelos acústicos en lenguas tonales.6 |
| **LASI-DAD** | India (12 idiomas: Hindi, Tamil, etc.) | 4,096 adultos. Pruebas cognitivas y de fluidez verbal. | **Público**: Disponible en *Gateway to Global Aging* (g2aging.org) previa creación de cuenta. | Dataset masivo que permite estudiar el efecto del multilingüismo en la demencia. |

### **2.4. Datasets Unificados (Frameworks 2025-2026)**

* **MultiConAD (2025):** Unifica 16 fuentes públicas (español, inglés, chino, griego). Es la base recomendada para iniciar cualquier investigación de validación cruzada.6  
* **SpeechDx (Barcelona Beta):** Consorcio global con 2,650 participantes, armonizando datos clínicos y de voz.

## ---

**3\. Oportunidades de Investigación y Publicación Q1 desde Perú**

Para lograr una publicación de alto impacto (Q1) en revistas como *Lancet Digital Health* o *Alzheimer's & Dementia* sin tener inicialmente un dataset local gigante, la literatura sugiere los siguientes caminos:

### **ESTRATEGIA A: Validación del "Sesgo de Acento" en IA (Impacto: Alto)**

**Hipótesis:** Los modelos entrenados con el dataset **Ivanova (España)** pierden un ![][image1] de precisión al aplicarse a grabaciones de adultos mayores peruanos debido a la prosodia y uso de muletillas regionales.3

* **Publicación:** "Cross-dialectal generalizability of Foundation Speech Models: A comparative study between Peninsular and Peruvian Spanish in AD detection."  
* **Valor agregado:** Sería el primer paper en cuantificar cuánto "ignora" la IA los matices fonéticos andinos o amazónicos.3

### **ESTRATEGIA B: El Nicho del Bilingüismo Indígena (Impacto: Muy Alto/Novedad)**

**Hipótesis:** El bilingüismo Quechua-Español actúa como una reserva cognitiva que altera los marcadores tradicionales de "silencios y pausas" en el habla.

* **Metodología:** Utilizar el framework **Voxlect** (identificador de dialectos) sobre población bilingüe en Arequipa o Cusco.4  
* **Publicación:** "Digital biomarkers of cognitive decline in Indigenous bilingual populations: Evidence from the Peruvian Andes."  
* **Revista Objetivo:** *Nature Mental Health* o *Scientific Reports*.

### **ESTRATEGIA C: Fusión Multimodal de Bajo Costo (Impacto: Clínico)**

**Hipótesis:** La combinación de **análisis de voz** (biomarcador conductual) con **biomarcadores de plasma (p-tau217)**, que ya se están estudiando en Perú, aumenta la precisión del diagnóstico temprano en un ![][image2].

* **Publicación:** "Multimodal integration of speech patterns and blood-based biomarkers for early Alzheimer’s screening in resource-limited settings."

## ---

**4\. Hoja de Ruta Crítica (Roadmap 2026\)**

1. **Abril \- Mayo 2026 (Fase de Datos Globales):** Solicitar acceso a **DementiaBank** y descargar **MultiConAD**. Entrenar un modelo base (Whisper-large o Wav2Vec 2.0) usando estas fuentes.6  
2. **Junio \- Agosto 2026 (Pilotaje Local):** Coordinar con el **GIEF (UPCH)** o el **Instituto de Neurociencias** en Lima para grabar a 30-50 sujetos peruanos usando el protocolo estandarizado de "Cookie Theft".17  
3. **Septiembre \- Noviembre 2026 (Análisis de Error):** Aplicar el modelo global a la data peruana. Identificar los "falsos positivos" causados por giros lingüísticos locales.2  
4. **Diciembre 2026 (Publicación):** Someter el artículo a una revista Q1 enfocándose en la **Equidad Médica** y la necesidad de modelos de IA culturalmente conscientes.

## ---

**5\. Conclusión: El valor de "Lo Nuestro"**

Para 2026, la IA ya no es una novedad; lo que las revistas Q1 buscan es **generalizabilidad**. Si logras demostrar que la IA actual falla o necesita ajustes para el adulto mayor peruano (especialmente el que vive en los Andes o la selva), estarás resolviendo un problema de **justicia algorítmica** que es de sumo interés para la comunidad científica global.3

**Contactos Estratégicos Recomendados:**

* **Dr. César Beltrán (PUCP):** Para la arquitectura de Deep Learning adaptada a Quechua.5  
* **Dra. Rosa Montesinos (UPCH):** Para la validación clínica y acceso a pacientes bajo el nuevo Plan Nacional.1  
* **Impact Salud:** Proyecto clave que ya está validando herramientas de mHealth en 4 regiones del Perú.3

#### **Fuentes citadas**

1. Perú da un paso histórico con su primer Plan Nacional de ..., acceso: abril 2, 2026, [https://impact-salud.org/en/peru-takes-a-historic-step-forward-with-its-first-national-dementia-plan/](https://impact-salud.org/en/peru-takes-a-historic-step-forward-with-its-first-national-dementia-plan/)  
2. VoxCog: Towards End-to-End Multilingual Cognitive Impairment Classification through Dialectal Knowledge \- arXiv, acceso: abril 2, 2026, [https://arxiv.org/html/2601.07999v1](https://arxiv.org/html/2601.07999v1)  
3. Validation and cost- effectiveness of an mHealth tool for cognitive impairment detection in Peru \- BMJ Open, acceso: abril 2, 2026, [https://bmjopen.bmj.com/content/bmjopen/15/11/e107142.full.pdf](https://bmjopen.bmj.com/content/bmjopen/15/11/e107142.full.pdf)  
4. MultiConAD: A Unified Multilingual Conversational Dataset for Early Alzheimer's Detection, acceso: abril 2, 2026, [https://www.semanticscholar.org/paper/MultiConAD%3A-A-Unified-Multilingual-Conversational-Shakeri-Farmanbar/0584885daee46d60a49f079082fff0c4d581d14d](https://www.semanticscholar.org/paper/MultiConAD%3A-A-Unified-Multilingual-Conversational-Shakeri-Farmanbar/0584885daee46d60a49f079082fff0c4d581d14d)  
5. CESAR ARMANDO BELTRAN CASTAÑON \- PUCP, acceso: abril 2, 2026, [https://www.pucp.edu.pe/profesor/cesar-beltran-castanon](https://www.pucp.edu.pe/profesor/cesar-beltran-castanon)  
6. Peru Approves Its National Dementia Plan: A Milestone for the Country and the Region, acceso: abril 2, 2026, [https://www.alzint.org/news-events/news/peru-approves-its-national-dementia-plan-a-milestone-for-the-country-and-the-region/](https://www.alzint.org/news-events/news/peru-approves-its-national-dementia-plan-a-milestone-for-the-country-and-the-region/)  
7. MultiConAD: A Unified Multilingual Conversational Dataset for Early Alzheimer's Detection, acceso: abril 2, 2026, [https://arxiv.org/html/2502.19208v1](https://arxiv.org/html/2502.19208v1)  
8. Investigaciones \- CESAR ARMANDO BELTRAN CASTAÑON, acceso: abril 2, 2026, [https://www.pucp.edu.pe/profesor/cesar-beltran-castanon/investigaciones/](https://www.pucp.edu.pe/profesor/cesar-beltran-castanon/investigaciones/)  
9. MultiConAD: A Unified Multilingual Conversational Dataset for Early Alzheimer's Detection \- Hugging Face, acceso: abril 2, 2026, [https://huggingface.co/papers/2502.19208](https://huggingface.co/papers/2502.19208)  
10. Speech Analysis as an Objective Biomarker in MDD Trials Speech Biomarkers for Alzheimer's Disease Show Promise Across Multiple Languages \- Cambridge Cognition, acceso: abril 2, 2026, [https://cambridgecognition.com/speech-analysis-as-an-objective-biomarker-in-mdd-trials-speech-biomarkers-for-alzheimers-disease-show-promise-across-multiple-languages/](https://cambridgecognition.com/speech-analysis-as-an-objective-biomarker-in-mdd-trials-speech-biomarkers-for-alzheimers-disease-show-promise-across-multiple-languages/)  
11. The Multi-Partner Consortium to Expand Dementia Research in Latin America (ReDLat): Driving Multicentric Research and Implementation Science \- ResearchGate, acceso: abril 2, 2026, [https://www.researchgate.net/publication/349993169\_The\_Multi-Partner\_Consortium\_to\_Expand\_Dementia\_Research\_in\_Latin\_America\_ReDLat\_Driving\_Multicentric\_Research\_and\_Implementation\_Science](https://www.researchgate.net/publication/349993169_The_Multi-Partner_Consortium_to_Expand_Dementia_Research_in_Latin_America_ReDLat_Driving_Multicentric_Research_and_Implementation_Science)  
12. VoxCog: Towards End-to-End Multilingual Cognitive Impairment Classification through Dialectal Knowledge \- ResearchGate, acceso: abril 2, 2026, [https://www.researchgate.net/publication/399734246\_VoxCog\_Towards\_End-to-End\_Multilingual\_Cognitive\_Impairment\_Classification\_through\_Dialectal\_Knowledge](https://www.researchgate.net/publication/399734246_VoxCog_Towards_End-to-End_Multilingual_Cognitive_Impairment_Classification_through_Dialectal_Knowledge)  
13. Automated Speech Markers of Alzheimer Dementia: Test of Cross-Linguistic Generalizability, acceso: abril 2, 2026, [https://www.jmir.org/2025/1/e74200](https://www.jmir.org/2025/1/e74200)  
14. ADI \- World Alzheimer Report 2025, acceso: abril 2, 2026, [https://www.alzint.org/resource/world-alzheimer-report-2025/](https://www.alzint.org/resource/world-alzheimer-report-2025/)  
15. Multimodal AI for Alzheimer Disease Diagnosis: Systematic Review ..., acceso: abril 2, 2026, [https://www.jmir.org/2026/1/e85414](https://www.jmir.org/2026/1/e85414)  
16. Early Alzheimer's Detection via Speech AI | PDF | Deep Learning \- Scribd, acceso: abril 2, 2026, [https://www.scribd.com/document/981598528/Research-Proposal](https://www.scribd.com/document/981598528/Research-Proposal)  
17. Noninvasive automatic detection of Alzheimer's disease from spontaneous speech: a review, acceso: abril 2, 2026, [https://www.frontiersin.org/journals/aging-neuroscience/articles/10.3389/fnagi.2023.1224723/full](https://www.frontiersin.org/journals/aging-neuroscience/articles/10.3389/fnagi.2023.1224723/full)  
18. Deep Multi-Modal Detection of Early Alzheimer's Disease (2025-2026) | Bass Connections, acceso: abril 2, 2026, [https://bassconnections.duke.edu/project/deep-multi-modal-detection-early-alzheimers-disease-2025-2026/](https://bassconnections.duke.edu/project/deep-multi-modal-detection-early-alzheimers-disease-2025-2026/)  
19. Bias in Large AI Models for Medicine and Healthcare: Survey and Challenges \- Preprints.org, acceso: abril 2, 2026, [https://www.preprints.org/manuscript/202511.1838](https://www.preprints.org/manuscript/202511.1838)  
20. ARXIV \[Abstract\_Paper\] CHI 2026 ASR Cognitive Impairment, acceso: abril 2, 2026, [https://arxiv.org/pdf/2602.23436](https://arxiv.org/pdf/2602.23436)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADgAAAAXCAYAAABefIz9AAACgElEQVR4Xu2XTchMURjHH0mRr3wUivQuUEhKUUpIxAKFImIjkQWSsLB42cgCZYEUdlaKjbxZMGHhY8GCLKxYWiiKhRL/33ue071zZu59Z1yDdP/1a+Y+58yd85zn49xrVqtWrd+gqeKyuClmJ2N5jRH9YmJi77nGiWmpUZokRqdGCwuMdubcF8vEeHFXHPfvaJgzV9wSW93ec7Gbi8UJ8Ukcax4eFLYf4oN473wUTy3bkA3ilZjs1zvEEXFSPBG3nWviohjh83quf8pBjMNTY0WtE0fFHvHVih3EIRx76ewSo5I5DQsbhta7LYpUhSties7epCUWcvugta+JKlokvlixgyy4THvFIzHWr5lPFBG1d8ZZ7bZCMXmBhUK9IGY4VdWJg2QPzQTSTJpnIbKzLKzxlJjvY5vFYYexjoVjOAk4TIS7ukFOQzl4T9wQV503Yqdl/8fnFgt1Sa0dcttMccmyFP1l0eKpJdJko7Xu8FAqc3Cftbb1leKzheZSJHoG5yJNLGqheCyeWaj/rsVNt4vX1kG+51TmYDvRPd+JO2JkMhZFSlKbiMYCDy2kLus8L/p8vCPReHZbuMk2K2jFBSpykLTqF6sSe3SwYVnnzIuonbVsDTQcYOPjUbLJKVUs+tNiQCy17tMTFTm4Qny31kiVRZBNoe6ovyjuCw0rPkqaNEdcz8F1FRU5SArRwKYkdmqQ+Wlt0lh4aKBz5hUj+FxMcBvRi0fJoIgMESJSRIzIVRUNJD6Z8LTyza/P5eawkAcWFnPAeSv2W2vXpu4571I7GwUvrKQG/3sH+TEdMv+I9KdEXa3J0e5M4+2CxtJuLGq5hbcONmxtMlarVq2/pJ8A15Ck8/dowAAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABoAAAAXCAYAAAAV1F8QAAAB0klEQVR4Xu2UPyiGURTGj/yJKAOFKF+yiEKSSRkoBgYlAxkYUDJYiIikJDbKIGUwSUj+Tv4NkpWMWJXBYMTzOOd+7/XyZftKeerXd++5ve8573POd0X+FSelgxlwACpDZ76KwEA46CsRlIA6I9U7SwJLoBNkgh0wIpqc4rOkAVyAYot/UwW4BhOgy9gFBXbOKm9Ble1bwBCYAudg3TgSLSam4pKIn3kHam3fa7yDZosxwaP9un2fralSYxEke/GoEkQP9yToCasn4yDXYuXgXoJE9aDb1mlg2YjZm3zRF3CaskATiBgswokDcAYaLU7byuyMX99hxFQ1eBWdolHRyreMeflqA/t4CjZFx5cJfbt+tMyJPWAvDkUtoGgPeQatFvtJzjLaxaSkHVyBDQls/xS9fhO1zinPeAArXjysHtBma1fcsWgLakQnMmo/rXoBwy4gXxNtgxTvzImWzUlgFwsla7bnH3waZNv+c3Ej2h+n374oQ9SyiBdjAocTE/E9UU2KNt9V52x4Er1SwhqUwDKnX7+I4ujug1XREb003GT54mW6IN8njAWRE9H3cUDGJPR83BJRvHlpF8c9xwiLQzELCsMHEox3vwTj7e7Jf/0BfQD59F5kX01DxgAAAABJRU5ErkJggg==>