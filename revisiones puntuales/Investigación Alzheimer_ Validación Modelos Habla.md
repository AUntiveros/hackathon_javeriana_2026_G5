# **Estrategia nacional de investigación para el diagnóstico de la enfermedad de Alzheimer mediante el análisis computacional del habla en el Perú (Abril 2026\)**

La convergencia entre la inteligencia artificial y la neurología clínica ha alcanzado un hito significativo en 2026, consolidando al análisis automatizado del habla y el lenguaje como una de las fronteras más prometedoras para la detección temprana de enfermedades neurodegenerativas. En el contexto peruano, esta transición tecnológica coincide con una urgencia epidemiológica sin precedentes. América Latina enfrenta una de las transiciones demográficas más rápidas de la historia mundial, con una proyección de que los casos de demencia se duplicarán cada 20 años, alcanzando los 18.7 millones de personas afectadas para el año 2050\.1 En respuesta a este desafío, el Ministerio de Salud del Perú ha oficializado el Plan Nacional para la Prevención y Tratamiento de la Enfermedad de Alzheimer y Otras Demencias 2026-2028, marcando el inicio de una política pública integral que reconoce el deterioro cognitivo como una prioridad de salud pública.3 Este informe detalla el marco técnico, metodológico y estratégico para la implementación de un sistema de diagnóstico basado en el habla, optimizado para la diversidad lingüística del territorio peruano y alineado con los estándares globales de publicación científica de alto impacto.

## **Contexto epidemiológico y el imperativo de la detección temprana en el Perú**

La enfermedad de Alzheimer (EA) representa entre el 60% y el 70% de los casos de demencia a nivel global, y su impacto en economías de ingresos medios como la peruana se ve agravado por diagnósticos tardíos y un acceso limitado a biomarcadores convencionales, como la tomografía por emisión de positrones (PET) o el análisis de líquido cefalorraquídeo.1 La fragilidad de los sistemas de salud en regiones rurales del Perú, donde la densidad de neurólogos es significativamente menor que el promedio regional, exige herramientas de tamizaje que sean no invasivas, de bajo costo y capaces de operar en entornos con recursos limitados.1

La literatura científica de 2025 y 2026 subraya que los cambios en los patrones del habla pueden preceder a los síntomas cognitivos evidentes por varios años.6 En el Perú, la diversidad geográfica y cultural —representada por la metrópoli de Lima, las zonas semiurbanas de la costa norte como Tumbes, los Andes centrales en Huancayo y la Amazonía en Iquitos— presenta un desafío único para la estandarización de estas herramientas.8 El Plan Nacional 2026-2028 busca precisamente descentralizar el diagnóstico, utilizando la tecnología móvil (mHealth) y el personal de salud comunitario como puentes para la detección temprana.3

| Indicador Epidemiológico | Valor Estimado (LatAm/Perú) | Proyección 2050 |
| :---- | :---- | :---- |
| Prevalencia de Demencia (60+) | 7.1% \- 8.5% 1 | \~18.7 millones (LatAm) 2 |
| Tasa de Duplicación de Casos | Cada 20 años 1 | Crecimiento exponencial |
| Gasto en Salud Mental | \< 3% del presupuesto total 1 | Necesidad de incremento al 5% |
| Densidad de Neurólogos | 0.5 \- 3.5 por 100,000 hab. 1 | Brecha crítica en zonas rurales |

## **Fundamentos neurobiológicos y marcadores biológicos del habla**

El deterioro del lenguaje en la EA no es un síntoma aislado, sino el resultado de la degradación de redes neuronales específicas que coordinan la memoria semántica, la función ejecutiva y el control motor fino. Los biomarcadores del habla se dividen fundamentalmente en dos categorías: rasgos acústicos (forma y sonido) y rasgos lingüísticos (contenido y estructura).5

### **Dinámica de los rasgos acústicos y temporales**

Los rasgos acústicos capturan la integridad de la producción vocal y la planificación motora. Los pacientes en etapas iniciales de EA y deterioro cognitivo leve (DCL) muestran una reducción medible en la velocidad de habla y un aumento en la duración y frecuencia de las pausas silenciosas.9 Estas pausas, a menudo denominadas "vacilaciones", reflejan la dificultad del cerebro para recuperar palabras (anomia) y la pérdida de fluidez en la conexión de ideas.5

Investigaciones recientes han demostrado que la inestabilidad en la frecuencia fundamental (![][image1]), medida a través de métricas como el *jitter* y el *shimmer*, sirve como un indicador de la degradación neuromuscular sutil.9 Además, se ha observado un fenómeno de "aplanamiento prosódico", donde la variabilidad del tono disminuye, resultando en un habla monótona que carece de la expresividad emocional característica de los adultos sanos.9

### **Transformaciones lexico-semánticas y sintácticas**

En el nivel lingüístico, la EA se manifiesta mediante una simplificación de la estructura gramatical y una reducción en la diversidad del vocabulario, fenómeno conocido como "habla vacía".9 Los pacientes tienden a reemplazar sustantivos específicos por pronombres genéricos ("eso", "aquello") y a utilizar palabras de contenido pobre.14 La densidad de unidades de contenido (Content Units) en tareas narrativas, como la descripción de la imagen del "Robo de las Cookies", disminuye significativamente a medida que progresa la enfermedad.14

| Rasgo Lingüístico | Descripción del Cambio en EA | Implicación Clínica |
| :---- | :---- | :---- |
| Ratio Tipo-Token (TTR) | Disminución de palabras únicas.9 | Reducción de la reserva lingüística. |
| Densidad de Pronombres | Aumento relativo frente a sustantivos.14 | Dificultad de acceso al léxico específico. |
| Longitud de Enunciado | Acortamiento de frases y sintaxis simple.9 | Compromiso de la memoria de trabajo. |
| Coherencia Semántica | Desconexión entre conceptos sucesivos.16 | Desintegración de la red semántica central. |

## **Estado del arte en inteligencia artificial para el diagnóstico (2025-2026)**

El campo del diagnóstico automatizado ha transitado de clasificadores estadísticos simples a modelos de cimentación (Foundation Models) de gran escala que integran representaciones multimodales. En 2026, la IA no solo clasifica muestras de audio, sino que actúa como un agente capaz de razonar sobre la trayectoria longitudinal del paciente.17

### **Modelos de cimentación y arquitecturas de audio**

Modelos como Whisper (OpenAI) y Wav2Vec 2.0 (Meta) se han convertido en el estándar para la extracción de características, gracias a su pre-entrenamiento en cientos de miles de horas de habla diversa.19 Estas arquitecturas permiten generar incrustaciones (embeddings) que capturan matices prosódicos y fonéticos imposibles de detectar mediante el oído humano o métodos manuales.19

Un avance crítico presentado en 2026 es el framework VoxCog, el cual integra el conocimiento dialectal explícito para mejorar la clasificación del deterioro cognitivo.22 La premisa de VoxCog es que los cambios en el habla producidos por la EA —como el alargamiento de fonemas y la ralentización del ritmo— comparten similitudes morfológicas con variaciones dialectales. Al inicializar un modelo con un clasificador de dialectos, se proporciona un "prior" robusto que mejora la precisión del diagnóstico en un 5-7% en comparación con modelos que no consideran la variación regional.22

### **Hacia una IA agéntica e interpretable**

La crítica persistente hacia los modelos de "caja negra" ha impulsado el desarrollo de sistemas interpretables. La arquitectura Mixture of Experts (MoE) permite que diferentes "expertos" dentro del modelo se especialicen en rasgos específicos (vocalizaciones, pausas, sintaxis), permitiendo rastrear la decisión diagnóstica hasta tokens o segmentos de audio particulares.12 En 2026, la frontera se sitúa en la "IA Agéntica", sistemas capaces de solicitar contexto adicional —como una nueva muestra de habla bajo una tarea de memoria específica— si la incertidumbre del diagnóstico inicial es alta.17

| Modelo | Exactitud Reportada (ADReSS/ADReSSo) | Características Clave |
| :---- | :---- | :---- |
| Whisper-medium | 0.731 (Acc), 0.802 (AUC) 20 | Robusto en condiciones de ruido. |
| VoxCog (End-to-End) | 0.875 (Acc), 0.859 (Acc) 22 | Usa conocimiento dialectal como prior. |
| Multimodal Transformer | F1 83.32, AUC 89.48 12 | Fusión de audio y texto. |
| GPT-4o fine-tuned | F1 0.82 21 | Alto rendimiento en análisis de transcripciones. |

## **Plan de investigación en el territorio peruano: Implementación y validación**

La investigación en el Perú debe capitalizar la infraestructura existente y los proyectos de colaboración internacional como IMPACT Salud y ReDLat (Multi-partner Consortium to Expand Dementia Research in Latin America).3 El plan se estructura en fases que garantizan la validez científica y la aplicabilidad clínica.

### **Fase 1: Recolección y armonización de datos multimodales**

La recolección de datos debe seguir protocolos estandarizados para asegurar la interoperabilidad con bases de datos globales como DementiaBank.15 Se utilizará la tarea de descripción de la imagen "Cookie Theft" como estímulo principal, complementada con tareas de fluidez verbal y lectura de párrafos estandarizados, los cuales han demostrado ser altamente efectivos para detectar rasgos prosódicos en español.25

El proyecto IMPACT Salud propone un modelo de tamizaje masivo utilizando una aplicación de mHealth en tabletas, administrada por trabajadores de salud comunitarios en cuatro regiones del Perú.8 Este enfoque permite capturar la variabilidad dialectal del español peruano (costeño, andino y amazónico), un factor crítico para evitar falsos positivos derivados de patrones de habla regionales.8

### **Fase 2: Desarrollo de modelos con Transfer Learning translingüístico**

Dada la escasez de grandes conjuntos de datos de EA etiquetados en español peruano, la estrategia central es el aprendizaje por transferencia (Transfer Learning). Este proceso implica tomar modelos pre-entrenados en idiomas con abundantes recursos, como el inglés y el mandarín, y adaptarlos al contexto local.29

La evidencia de 2025 indica que, aunque los rasgos léxicos no siempre se transfieren bien entre idiomas debido a diferencias gramaticales, los rasgos de temporización (timing) son notablemente consistentes.16 Por ejemplo, los modelos entrenados en inglés que utilizan exclusivamente la duración de pausas y la tasa de habla han logrado un AUC de 0.75 al ser probados en hablantes de español sin re-entrenamiento previo.16

#### **Transferencia desde el inglés y lenguas asiáticas**

Se propone utilizar el framework Whisper-MJT (Multilingual Joint Training), que aprovecha las características de audio compartidas para construir modelos pre-entrenados multilingües.30 Al incluir transcripciones completas como "prompts" durante el ajuste fino (fine-tuning), se ha reportado una mejora en la precisión de un 4-7% en idiomas de bajos recursos.30

| Estrategia de Transferencia | Origen | Objetivo | Beneficio Esperado |
| :---- | :---- | :---- | :---- |
| Zero-shot Cross-lingual | Inglés / Mandarín | Español | Uso de espacios semánticos compartidos.32 |
| Fine-tuning con LoRA | Modelos Globales | Dialectos Peruanos | Adaptación eficiente con pocos datos.22 |
| Inicialización Dialectal | Voxlect (Dialectos) | Clasificación EA | Mejora de la robustez fonética.23 |

## **Validación cruzada de modelos y oportunidades en multilingüismo**

La validación cruzada (Cross-Validation) es el mecanismo esencial para garantizar que el modelo sea generalizable y no esté sobreajustado a una población específica. En el Perú, esto implica no solo validar entre regiones, sino también abordar la brecha de las lenguas indígenas, principalmente el Quechua.

### **El desafío del multilingüismo y las lenguas indígenas**

El Grupo de Inteligencia Artificial de la Pontificia Universidad Católica del Perú (PUCP), liderado por César Beltrán Castañón, ha desarrollado recursos lingüísticos para el procesamiento computacional del Quechua sureño (Proyecto TARPURIQ).33 Existe una oportunidad de investigación de vanguardia en la creación de modelos de detección de EA que operen en entornos de alternancia de códigos (code-switching) o en poblaciones bilingües Quechua-Español. Los modelos de lenguaje adaptados como BERT-LID (Language Identification) pueden ser integrados para segmentar el habla antes de la extracción de biomarcadores.26

### **Validación cruzada entre corpora globales y locales**

Para alcanzar la robustez necesaria para la implementación clínica, los modelos desarrollados en el Perú deben ser validados contra el dataset MultiConAD, que unifica 16 bases de datos de demencia en inglés, español, chino y griego.29 Esta validación cruzada permite identificar qué marcadores son universales y cuáles son culturalmente específicos. Por ejemplo, los resultados de MultiConAD sugieren que mientras el chino se beneficia de modelos densos de representación de texto, el español muestra un mejor desempeño con clasificadores de árboles de decisión en entornos de entrenamiento multilingüe.37

## **Estrategias de publicación en revistas Q1/Q2 y posicionamiento científico**

La publicación de resultados en revistas de alto impacto no es solo una validación académica, sino una necesidad para atraer financiamiento internacional y asegurar que las innovaciones peruanas influyan en las guías clínicas globales.

### **Identificación de objetivos y criterios de rigor**

Para revistas del primer cuartil (Q1) como *Lancet Digital Health*, *Alzheimer's & Dementia* o *Journal of Medical Internet Research* (JMIR), la investigación debe ir más allá de reportar una alta precisión. Se requiere:

1. **Transparencia Metodológica**: Adhesión estricta a guías como PRISMA y QUADAS-2 para evaluar el riesgo de sesgo.19  
2. **Validez Externa**: Pruebas en conjuntos de datos independientes y geográficamente diversos (por ejemplo, validación cruzada entre Lima e Iquitos).8  
3. **Análisis de Equidad**: Evaluación del desempeño del modelo según niveles educativos, género y edad, asegurando que la IA no perpetúe desigualdades existentes.38

| Revista Objetivo | Factor de Impacto / Q | Temas Prioritarios (2025-2026) |
| :---- | :---- | :---- |
| *Lancet Digital Health* | Q1 | Validación clínica a escala, impacto en políticas.19 |
| *Alzheimer's & Dementia* | Q1 | Nuevos biomarcadores digitales y longitudinales.9 |
| *JMIR AI* | Q1/Q2 | LLMs en salud mental, adaptación de modelos.21 |
| *Scientific Reports* | Q1 | Fusión multimodal y algoritmos explicables.19 |

### **Narrativa de la investigación para el éxito editorial**

Las publicaciones exitosas en 2026 enfatizan la "traducción clínica". En lugar de presentar un modelo puramente técnico, los investigadores peruanos deben estructurar sus artículos enfocándose en cómo la herramienta ASLA (Automated Speech and Language Analysis) complementa la evaluación neuropsicológica tradicional (como el MMSE) y reduce la carga del sistema de salud.10 La inclusión de "justificaciones narrativas" generadas por IA que expliquen por qué un paciente fue clasificado como DCL es un diferenciador clave que los revisores de Q1 valoran actualmente.18

## **Ética, sesgo y desafíos de la implementación en el mundo real**

El despliegue de sistemas de IA para el diagnóstico de Alzheimer conlleva responsabilidades éticas críticas. La literatura de 2026 advierte sobre el "sesgo médico" en modelos de gran escala que, a menudo, han sido entrenados mayoritariamente en poblaciones anglosajonas y caucásicas.39

### **Mitigación de sesgos y protección de datos**

En el Perú, la diversidad de niveles de alfabetización y la calidad educativa varían drásticamente. Un modelo que no esté calibrado para estas variables podría confundir un nivel educativo bajo con un deterioro cognitivo.8 Por ello, es imperativo integrar variables sociodemográficas como covariables en los modelos predictivos.38

Desde el punto de vista de la privacidad, el análisis del habla es particularmente sensible, ya que la voz es un identificador biométrico. El plan de investigación debe contemplar el uso de técnicas de privacidad diferencial o computación federada, permitiendo que los modelos se entrenen en los dispositivos locales (Edge AI) sin necesidad de subir el audio crudo a la nube, cumpliendo así con las normativas peruanas de protección de datos personales.6

### **El rol del cuidador y el sistema de salud**

La implementación exitosa requiere que la tecnología no sea vista como un reemplazo, sino como un apoyo al clínico. El Plan Nacional 2026-2028 enfatiza el apoyo a los cuidadores informales, quienes realizan aproximadamente el 50% de las tareas de cuidado a nivel global.41 Los sistemas de habla pueden integrarse en aplicaciones de monitoreo remoto que alerten a los cuidadores y médicos sobre cambios sutiles en la trayectoria cognitiva del paciente en el hogar, permitiendo ajustes oportunos en el plan de cuidados.5

## **Conclusiones y recomendaciones para la agenda 2026**

La investigación peruana en el diagnóstico del habla para la enfermedad de Alzheimer se encuentra en una posición privilegiada para liderar el cambio en la región. La combinación de un marco político favorable, la participación de instituciones académicas de prestigio como la PUCP y la UPCH, y la disponibilidad de tecnologías de IA de vanguardia, crea un ecosistema propicio para la innovación.

Las recomendaciones estratégicas finales para el equipo de investigación incluyen:

1. **Priorizar el Transfer Learning Dialectal**: Adoptar arquitecturas como VoxCog para neutralizar el efecto de los acentos regionales peruanos en el diagnóstico.  
2. **Fomentar la Multimodalidad**: No depender exclusivamente del habla; la integración de datos clínicos, comorbilidades y, cuando sea posible, biomarcadores de plasma, aumentará la precisión en un margen de hasta seis puntos porcentuales.8  
3. **Compromiso con la Ciencia Abierta**: Contribuir a repositorios como Zenodo y Harvard Dataverse con datasets armonizados del contexto peruano para fomentar la validación cruzada global y aumentar el impacto de las citaciones.1  
4. **Enfoque en la Atención Primaria**: Diseñar herramientas que puedan ser utilizadas por trabajadores de salud no especializados, alineándose con el objetivo de descentralización del Ministerio de Salud.3

En última instancia, el éxito de este plan de investigación no se medirá solo por la precisión de sus algoritmos, sino por su capacidad para transformar el habla cotidiana en una herramienta de esperanza y cuidado, permitiendo que miles de peruanos reciban el apoyo que necesitan antes de que la memoria se desvanezca por completo. La meta para abril de 2026 es clara: convertir la voz en el biomarcador más accesible y democrático para la salud cerebral del Perú.

#### **Fuentes citadas**

1. Alzheimer's Disease Evolution in Latin America ... \- Zenodo, acceso: abril 2, 2026, [https://zenodo.org/records/19124882/files/P01\_AlzheimerLatAm\_DatasetDescriptor\_bioRxiv.pdf?download=1](https://zenodo.org/records/19124882/files/P01_AlzheimerLatAm_DatasetDescriptor_bioRxiv.pdf?download=1)  
2. Press Release: Latin America Faces Alzheimer Crisis — New Open Dataset Projects 18.7 Million Cases by 2050 \- Zenodo, acceso: abril 2, 2026, [https://zenodo.org/records/19125114](https://zenodo.org/records/19125114)  
3. Perú da un paso histórico con su primer Plan Nacional de ..., acceso: abril 2, 2026, [https://impact-salud.org/en/peru-takes-a-historic-step-forward-with-its-first-national-dementia-plan/](https://impact-salud.org/en/peru-takes-a-historic-step-forward-with-its-first-national-dementia-plan/)  
4. Peru Approves Its National Dementia Plan: A Milestone for the Country and the Region, acceso: abril 2, 2026, [https://www.alzint.org/news-events/news/peru-approves-its-national-dementia-plan-a-milestone-for-the-country-and-the-region/](https://www.alzint.org/news-events/news/peru-approves-its-national-dementia-plan-a-milestone-for-the-country-and-the-region/)  
5. MultiConAD: A Unified Multilingual Conversational Dataset for Early Alzheimer's Detection | Request PDF \- ResearchGate, acceso: abril 2, 2026, [https://www.researchgate.net/publication/393657688\_MultiConAD\_A\_Unified\_Multilingual\_Conversational\_Dataset\_for\_Early\_Alzheimer's\_Detection](https://www.researchgate.net/publication/393657688_MultiConAD_A_Unified_Multilingual_Conversational_Dataset_for_Early_Alzheimer's_Detection)  
6. SpeechDx \- Alzheimer's Drug Discovery Foundation, acceso: abril 2, 2026, [https://www.alzdiscovery.org/research-and-grants/speechdx](https://www.alzdiscovery.org/research-and-grants/speechdx)  
7. AI Shows Promise for Detecting Early Cognitive Decline through Speech Samples, acceso: abril 2, 2026, [https://medicine.wsu.edu/news/2026/03/17/ai-shows-promise-for-detecting-early-cognitive-decline-through-speech/](https://medicine.wsu.edu/news/2026/03/17/ai-shows-promise-for-detecting-early-cognitive-decline-through-speech/)  
8. Validation and cost- effectiveness of an mHealth tool for cognitive impairment detection in Peru \- BMJ Open, acceso: abril 2, 2026, [https://bmjopen.bmj.com/content/bmjopen/15/11/e107142.full.pdf](https://bmjopen.bmj.com/content/bmjopen/15/11/e107142.full.pdf)  
9. Early Alzheimer's Detection via Speech AI | PDF | Deep Learning \- Scribd, acceso: abril 2, 2026, [https://www.scribd.com/document/981598528/Research-Proposal](https://www.scribd.com/document/981598528/Research-Proposal)  
10. LSU Research Bites: AI Analysis of Everyday Speech Helps Detect Dementia Earlier, acceso: abril 2, 2026, [https://www.lsu.edu/blog/2025/11/rb-dementia-ai.php](https://www.lsu.edu/blog/2025/11/rb-dementia-ai.php)  
11. Developing a Multimodal Screening Algorithm for Mild Cognitive Impairment and Early Dementia in Home Health Care: Protocol for a Cross-Sectional Case-Control Study Using Speech Analysis, Large Language Models, and Electronic Health Records, acceso: abril 2, 2026, [https://www.researchprotocols.org/2026/1/e82731](https://www.researchprotocols.org/2026/1/e82731)  
12. Speech and Language Foundation Models for Accurate and Interpretable Alzheimer's Dementia Recognition \- Apollo, acceso: abril 2, 2026, [https://www.repository.cam.ac.uk/items/437875e8-129a-4d93-a8cd-a0f9cd4b3a16](https://www.repository.cam.ac.uk/items/437875e8-129a-4d93-a8cd-a0f9cd4b3a16)  
13. Speech Analysis by Natural Language Processing Techniques: A Possible Tool for Very Early Detection of Cognitive Decline? \- Frontiers, acceso: abril 2, 2026, [https://www.frontiersin.org/journals/aging-neuroscience/articles/10.3389/fnagi.2018.00369/full](https://www.frontiersin.org/journals/aging-neuroscience/articles/10.3389/fnagi.2018.00369/full)  
14. Speech Analysis as an Objective Biomarker in MDD Trials Speech Biomarkers for Alzheimer's Disease Show Promise Across Multiple Languages \- Cambridge Cognition, acceso: abril 2, 2026, [https://cambridgecognition.com/speech-analysis-as-an-objective-biomarker-in-mdd-trials-speech-biomarkers-for-alzheimers-disease-show-promise-across-multiple-languages/](https://cambridgecognition.com/speech-analysis-as-an-objective-biomarker-in-mdd-trials-speech-biomarkers-for-alzheimers-disease-show-promise-across-multiple-languages/)  
15. Noninvasive automatic detection of Alzheimer's disease from spontaneous speech: a review, acceso: abril 2, 2026, [https://www.frontiersin.org/journals/aging-neuroscience/articles/10.3389/fnagi.2023.1224723/full](https://www.frontiersin.org/journals/aging-neuroscience/articles/10.3389/fnagi.2023.1224723/full)  
16. Automated Speech Markers of Alzheimer Dementia: Test of Cross-Linguistic Generalizability, acceso: abril 2, 2026, [https://www.jmir.org/2025/1/e74200](https://www.jmir.org/2025/1/e74200)  
17. AI agents in Alzheimer's disease management: challenges and future directions \- Frontiers, acceso: abril 2, 2026, [https://www.frontiersin.org/journals/aging-neuroscience/articles/10.3389/fnagi.2025.1735892/full](https://www.frontiersin.org/journals/aging-neuroscience/articles/10.3389/fnagi.2025.1735892/full)  
18. AI agents in Alzheimer's disease management: challenges and ..., acceso: abril 2, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12812870/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12812870/)  
19. Multimodal AI for Alzheimer Disease Diagnosis: Systematic Review ..., acceso: abril 2, 2026, [https://www.jmir.org/2026/1/e85414](https://www.jmir.org/2026/1/e85414)  
20. Benchmarking Foundation Models for Alzheimer's Disease and Related Dementia Detection from Spontaneous Speech \- PMC, acceso: abril 2, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12763132/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12763132/)  
21. Large Language Model Adaptation Strategies in Speech- Based Cognitive Screening: Systematic Evaluation \- JMIR AI, acceso: abril 2, 2026, [https://ai.jmir.org/2026/1/e82608/PDF](https://ai.jmir.org/2026/1/e82608/PDF)  
22. VoxCog: Towards End-to-End Multilingual Cognitive Impairment Classification through Dialectal Knowledge \- arXiv, acceso: abril 2, 2026, [https://arxiv.org/html/2601.07999v1](https://arxiv.org/html/2601.07999v1)  
23. VoxCog: Towards End-to-End Multilingual Cognitive Impairment Classification through Dialectal Knowledge \- ResearchGate, acceso: abril 2, 2026, [https://www.researchgate.net/publication/399734246\_VoxCog\_Towards\_End-to-End\_Multilingual\_Cognitive\_Impairment\_Classification\_through\_Dialectal\_Knowledge](https://www.researchgate.net/publication/399734246_VoxCog_Towards_End-to-End_Multilingual_Cognitive_Impairment_Classification_through_Dialectal_Knowledge)  
24. The Multi-Partner Consortium to Expand Dementia Research in Latin America (ReDLat): Driving Multicentric Research and Implementation Science \- ResearchGate, acceso: abril 2, 2026, [https://www.researchgate.net/publication/349993169\_The\_Multi-Partner\_Consortium\_to\_Expand\_Dementia\_Research\_in\_Latin\_America\_ReDLat\_Driving\_Multicentric\_Research\_and\_Implementation\_Science](https://www.researchgate.net/publication/349993169_The_Multi-Partner_Consortium_to_Expand_Dementia_Research_in_Latin_America_ReDLat_Driving_Multicentric_Research_and_Implementation_Science)  
25. (PDF) Discriminating speech traits of Alzheimer's disease assessed through a corpus of reading task for Spanish language \- ResearchGate, acceso: abril 2, 2026, [https://www.researchgate.net/publication/356793301\_Discriminating\_speech\_traits\_of\_Alzheimer's\_disease\_assessed\_through\_a\_corpus\_of\_reading\_task\_for\_Spanish\_language](https://www.researchgate.net/publication/356793301_Discriminating_speech_traits_of_Alzheimer's_disease_assessed_through_a_corpus_of_reading_task_for_Spanish_language)  
26. PPGs-BERT: Leveraging Phoneme Sequence and BERT for Alzheimer's Disease Detection from Spontaneous Speech | Request PDF \- ResearchGate, acceso: abril 2, 2026, [https://www.researchgate.net/publication/396810683\_PPGs-BERT\_Leveraging\_Phoneme\_Sequence\_and\_BERT\_for\_Alzheimer's\_Disease\_Detection\_from\_Spontaneous\_Speech](https://www.researchgate.net/publication/396810683_PPGs-BERT_Leveraging_Phoneme_Sequence_and_BERT_for_Alzheimer's_Disease_Detection_from_Spontaneous_Speech)  
27. Automated Speech Markers of Alzheimer Dementia: Test of Cross-Linguistic Generalizability, acceso: abril 2, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12572752/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12572752/)  
28. Peru Approves National Dementia Plan, Marking an Important Step Forward for Brain Health, acceso: abril 2, 2026, [https://www.gbhi.org/news-publications/peru-approves-national-dementia-plan-marking-important-step-forward-brain-health](https://www.gbhi.org/news-publications/peru-approves-national-dementia-plan-marking-important-step-forward-brain-health)  
29. MultiConAD: A Unified Multilingual Conversational Dataset for Early Alzheimer's Detection, acceso: abril 2, 2026, [https://www.semanticscholar.org/paper/MultiConAD%3A-A-Unified-Multilingual-Conversational-Shakeri-Farmanbar/0584885daee46d60a49f079082fff0c4d581d14d](https://www.semanticscholar.org/paper/MultiConAD%3A-A-Unified-Multilingual-Conversational-Shakeri-Farmanbar/0584885daee46d60a49f079082fff0c4d581d14d)  
30. Whisper-Based Multilingual Alzheimer's Disease Detection and Improvements for Low-Resource Language \- ISCA Archive, acceso: abril 2, 2026, [https://www.isca-archive.org/interspeech\_2025/jia25\_interspeech.pdf](https://www.isca-archive.org/interspeech_2025/jia25_interspeech.pdf)  
31. Automated Speech Markers of Alzheimer Dementia: Test of Cross-Linguistic Generalizability, acceso: abril 2, 2026, [https://pubmed.ncbi.nlm.nih.gov/41091545/](https://pubmed.ncbi.nlm.nih.gov/41091545/)  
32. Cross-Lingual Transfer Learning for Speech Translation \- ACL Anthology, acceso: abril 2, 2026, [https://aclanthology.org/2025.naacl-short.4/](https://aclanthology.org/2025.naacl-short.4/)  
33. CESAR ARMANDO BELTRAN CASTAÑON \- PUCP, acceso: abril 2, 2026, [https://www.pucp.edu.pe/profesor/cesar-beltran-castanon](https://www.pucp.edu.pe/profesor/cesar-beltran-castanon)  
34. Investigaciones \- CESAR ARMANDO BELTRAN CASTAÑON, acceso: abril 2, 2026, [https://www.pucp.edu.pe/profesor/cesar-beltran-castanon/investigaciones/](https://www.pucp.edu.pe/profesor/cesar-beltran-castanon/investigaciones/)  
35. MultiConAD: A Unified Multilingual Conversational Dataset for Early Alzheimer's Detection \- Hugging Face, acceso: abril 2, 2026, [https://huggingface.co/papers/2502.19208](https://huggingface.co/papers/2502.19208)  
36. MultiConAD: A Unified Multilingual Conversational Dataset for Early Alzheimer's Detection, acceso: abril 2, 2026, [https://arxiv.org/html/2502.19208v1](https://arxiv.org/html/2502.19208v1)  
37. MultiConAD: A Unified Multilingual Conversational Dataset for Early Alzheimer's Detection \- ChatPaper, acceso: abril 2, 2026, [https://chatpaper.com/paper/169789](https://chatpaper.com/paper/169789)  
38. Deep Multi-Modal Detection of Early Alzheimer's Disease (2025-2026) | Bass Connections, acceso: abril 2, 2026, [https://bassconnections.duke.edu/project/deep-multi-modal-detection-early-alzheimers-disease-2025-2026/](https://bassconnections.duke.edu/project/deep-multi-modal-detection-early-alzheimers-disease-2025-2026/)  
39. Bias in Large AI Models for Medicine and Healthcare: Survey and Challenges \- Preprints.org, acceso: abril 2, 2026, [https://www.preprints.org/manuscript/202511.1838](https://www.preprints.org/manuscript/202511.1838)  
40. ARXIV \[Abstract\_Paper\] CHI 2026 ASR Cognitive Impairment, acceso: abril 2, 2026, [https://arxiv.org/pdf/2602.23436](https://arxiv.org/pdf/2602.23436)  
41. ADI \- World Alzheimer Report 2025, acceso: abril 2, 2026, [https://www.alzint.org/resource/world-alzheimer-report-2025/](https://www.alzint.org/resource/world-alzheimer-report-2025/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAZCAYAAAAxFw7TAAABNklEQVR4XmNgGAWDHiQD8SwiMEgdQcAIxMJA7AnFP4G4H4glkbAtEJ8H4oVQPUSBaCj+B8QuaHIgEATE5eiCuADIlfOh+AkQy0DFmYGYF8r2ZYBYSBQQBOLTULwViDmg4sZAnAtl6wKxJpRNEIA0foXiTgZIuIE0b2DA7n2CIJ0BEnYgvJ4BEqOHgfgZECtB1YCCBeTliUgYxAeJYwCqGgiLEFBkIEcIyNvTGBDhqc0ASTacUMwDxCuAWB0qDwciQHyVARIZyBEiy4AafiDXoKdDEB8j5mERUgXFuAAoDWIzECNtwsIP5Bp8MUrQQFDKfwTEv4D4PxC/guILQKwFU4QEihiwGwhyEFnAEohXMkDCGIZBfJA4WYCVAZLofZAwiA8SJxuAkhioZIJhjDRIKqC6gUMYAACfJUWCH2rvrgAAAABJRU5ErkJggg==>