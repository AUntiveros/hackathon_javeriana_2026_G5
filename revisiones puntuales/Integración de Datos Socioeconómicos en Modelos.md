# **Integración de Perfiles Socioeconómicos y Evaluación de Equidad en Modelos de Detección de Enfermedades Neurodegenerativas: Un Marco para la Mitigación de Sesgos y la Optimización del Rendimiento Predictivo**

El desarrollo de sistemas de inteligencia artificial (IA) para la detección temprana de la enfermedad de Alzheimer y otras demencias relacionadas (ADRD) se encuentra en un punto de inflexión crítico. A medida que la prevalencia de estos trastornos cognitivos se proyecta para triplicarse hacia el año 2050, la necesidad de herramientas de tamizaje escalables y no invasivas se vuelve imperativa.1 Sin embargo, la precisión y la utilidad clínica de estos modelos están intrínsecamente ligadas a la calidad y representatividad de los datos de entrenamiento. Un desafío persistente en este ámbito es la omisión de los determinantes sociales de la salud (SDOH) y, específicamente, del nivel socioeconómico (SES) como variables de entrada fundamentales.3 La evidencia sugiere que el SES influye no solo en el riesgo biológico de padecer demencia a través de mecanismos de reserva cognitiva, sino también en los patrones lingüísticos y de comportamiento que los modelos de aprendizaje automático (ML) intentan decodificar.5

La integración de perfiles socioeconómicos en los modelos predictivos no es solo una cuestión de equidad ética, sino una necesidad técnica para reducir el error algorítmico. Los modelos agnósticos al contexto socioeconómico tienden a exhibir tasas de error desproporcionadamente altas en poblaciones vulnerables, lo que puede llevar a diagnósticos erróneos o a la exclusión de grupos históricamente desatendidos.3 Para abordar esta problemática, es fundamental explorar la arquitectura de los conjuntos de datos existentes, las metodologías de vinculación de metadatos espaciales y las estrategias de mitigación de sesgos durante el ciclo de vida del modelo.

## **Infraestructura de Datos y Metadatos Socioeconómicos en Estudios Globales de Envejecimiento**

La posibilidad de integrar indicadores socioeconómicos depende en gran medida de la granularidad de los metadatos disponibles en los repositorios de investigación. En los últimos años, se ha producido un avance significativo hacia la armonización de datos, permitiendo comparaciones transnacionales entre diversos estudios de cohortes.8

### **El Modelo de LASI-DAD y la Riqueza Epidemiológica**

El estudio Longitudinal Aging Study in India \- Diagnostic Assessment of Dementia (LASI-DAD) constituye uno de los ejemplos más robustos de cómo integrar datos socioeconómicos a gran escala.8 Este estudio, representativo a nivel nacional en la India, no solo recopila pruebas neuropsicológicas exhaustivas, sino que se vincula con la encuesta LASI principal, que abarca a más de 70,000 individuos.8 La estructura de LASI-DAD permite acceder a una profundidad de datos socioeconómicos que rara vez se encuentra en conjuntos de datos clínicos puros.

| Variable Socioeconómica | Descripción y Alcance en LASI-DAD | Impacto en el Modelado de IA |
| :---- | :---- | :---- |
| **Educación Formal** | Años de escolaridad del participante, padre y madre. | Permite ajustar los umbrales de normalidad en pruebas cognitivas. |
| **Ocupación de Vida** | Nivel de habilidad ocupacional y tipo de trabajo principal. | Indicador crítico de la reserva cognitiva y exposición a riesgos ambientales. |
| **Recursos Económicos** | Ingresos del hogar, consumo y activos (riqueza). | Proporciona contexto sobre el acceso a servicios de salud y nutrición. |
| **Entorno Urbano/Rural** | Clasificación geográfica de la residencia. | Crucial para evaluar el impacto de la contaminación y el acceso a infraestructura. |

8

La integración de estas variables permite a los investigadores realizar análisis estratificados. Por ejemplo, en LASI-DAD, el 62% de la cohorte no posee educación formal, lo que ha obligado a adaptar instrumentos como el Hindi Mental State Exam (HMSE) para evitar sesgos educativos en la evaluación de la memoria y la orientación.10 Para un modelo de ML, contar con el nivel educativo como "data de entrada" permite que el algoritmo aprenda que ciertos patrones de respuesta —que en una población altamente educada podrían interpretarse como deterioro— son normales dentro de un contexto de baja escolaridad.11

### **MultiConAD y la Dimensión Lingüística Multilingüe**

En el ámbito del análisis del habla, el dataset MultiConAD (Unified Multilingual Conversational Dataset), cuya publicación se consolida hacia 2025, representa un avance en la unificación de 16 conjuntos de datos conversacionales en idiomas como inglés, español, chino y griego.13 Aunque su enfoque primario es el audio y el texto, la metadata asociada incluye variables demográficas esenciales como la edad, el sexo y las puntuaciones de MMSE.15

La vinculación de SES en MultiConAD se realiza a menudo de forma indirecta a través de los datos de educación presentes en los datasets fuente, como el Pitt Corpus de DementiaBank.13 En el Pitt Corpus, el archivo de metadatos incluye niveles educativos categorizados (Primaria, Secundaria, Pregrado, Posgrado), lo cual es vital para evaluar si los biomarcadores lingüísticos, como la densidad proposicional o la complejidad sintáctica, varían sistemáticamente con el nivel socioeconómico.16

## **Metodologías para la Vinculación de Metadatos con Índices de Desarrollo Humano (IDH)**

Una de las preguntas centrales en la investigación actual es cómo enriquecer los datasets clínicos cuando los datos socioeconómicos individuales son escasos. La respuesta reside en el uso de medidas a nivel de área (area-level measures), vinculando la ubicación geográfica de los participantes con índices externos.18

### **El Uso del IDH y Clústeres Geográficos**

El Índice de Desarrollo Humano (IDH) es una medida compuesta que sintetiza la salud, la educación y el nivel de vida de una región determinada.20 El cálculo de este índice se basa en transformar indicadores con diferentes unidades en índices normalizados entre 0 y 1 mediante la fórmula:

![][image1]  
Para un investigador que trabaja con datos de Perú, por ejemplo, es posible utilizar el Informe sobre Desarrollo Humano 2025 del PNUD, que actualiza el IDH a nivel distrital hasta el año 2024\.21 Al disponer de la ubicación (distrito) en los metadatos del paciente, se puede asignar un clúster de IDH al registro clínico. Esta técnica permite que el modelo de IA capture la "vulnerabilidad del entorno", reconociendo que vivir en un distrito con bajo IDH puede estar asociado a una mayor carga de enfermedades crónicas no transmisibles, como la hipertensión y la diabetes, que a su vez son factores de riesgo para la demencia.23

### **El Índice de Privación de Área (ADI) y el SVI**

En contextos donde se requiere una mayor granularidad, el Area Deprivation Index (ADI) proporciona una visión detallada de la desventaja del vecindario.19 El ADI combina 17 indicadores del censo, incluyendo ingresos, empleo, vivienda y educación, a nivel de grupo de manzanas (census block groups).19

| Categoría del ADI | Indicadores Clave Incluidos | Relevancia para el Performance del Modelo |
| :---- | :---- | :---- |
| **Pobreza** | % de familias bajo el nivel de pobreza; % de hogares sin vehículo. | Identifica barreras para el seguimiento clínico y diagnóstico temprano. |
| **Vivienda** | Mediana del valor de la vivienda; hogares con hacinamiento. | Proxy de la calidad del entorno y exposición a factores estresantes. |
| **Educación** | % de población de 25+ años con \< 9 años de educación. | Ajusta la interpretación de biomarcadores cognitivos y lingüísticos. |
| **Empleo** | Tasa de desempleo; % de empleados en trabajos "blue-collar". | Refleja la estabilidad económica y la complejidad cognitiva laboral. |

19

La integración técnica de estos índices se facilita mediante herramientas como el paquete ezADI en R, que permite el geocodificado por lotes de direcciones y la unión con las puntuaciones de ADI.19 Este enfoque es particularmente útil para detectar sesgos algorítmicos: si un modelo presenta un error significativamente mayor en pacientes de áreas con alto ADI, esto indica que el modelo no ha capturado correctamente las variaciones fenotípicas o lingüísticas propias de esos entornos.3

## **Mecanismos de Sesgo Socioeconómico en el Modelado de IA para Salud**

La exclusión de datos socioeconómicos como variables de entrada no neutraliza el sesgo, sino que a menudo lo oculta. Los modelos entrenados en datos sesgados pueden perpetuar disparidades en la salud, especialmente en poblaciones subrepresentadas.7

### **El Sesgo de "Negado de Legado" y la Deriva de Datos**

Un fenómeno crítico es el llamado "sesgo de legado negativo", donde las inequidades históricas se reflejan en las etiquetas de diagnóstico del dataset.7 Por ejemplo, los pacientes de grupos socioeconómicos bajos suelen tener un acceso tardío a los especialistas, lo que resulta en diagnósticos de demencia en etapas más avanzadas en comparación con pacientes de SES alto que reciben tamizajes preventivos.7 Si un modelo de IA aprende de estos datos sin considerar el SES, puede asociar erróneamente ciertos marcadores lingüísticos sutiles —que son normales en ciertos dialectos o niveles educativos— con una etapa avanzada de la enfermedad.27

Además, el rendimiento de los modelos suele degradarse debido a la baja calidad de los registros electrónicos de salud (EHR) en centros de atención para poblaciones de bajos recursos, donde los datos pueden estar incompletos o ser menos precisos.3 Las investigaciones indican que el uso de una medida de SES a nivel individual (como el HOUSES Index) es a veces más eficaz para detectar y mitigar este sesgo que las medidas a nivel de área, ya que captura la situación específica del paciente que interactúa con el sistema de salud.3

### **Impacto en la Detección basada en el Habla**

En los modelos que utilizan biomarcadores de voz y lenguaje, el nivel educativo es el principal factor de confusión. Las métricas de riqueza léxica, como el Yule's K, y la diversidad de vocabulario están fuertemente influenciadas por la formación académica.15 En un análisis de pacientes con deterioro cognitivo leve (MCI), se observó que el habla se caracteriza por una menor diversidad léxica y oraciones más largas, patrones que también pueden solaparse con características del habla en individuos con baja escolaridad.15 Sin la inclusión de perfiles socioeconómicos, el modelo corre el riesgo de generar falsos positivos en personas con poca educación formal, simplemente por la similitud en la estructura superficial de su discurso.27

## **Estrategias de Aprendizaje Automático Consciente de la Equidad (Fairness-aware ML)**

Para limitar los sesgos mencionados, la literatura técnica propone tres enfoques de intervención: pre-procesamiento, procesamiento (in-processing) y post-procesamiento.29

### **Mitigación en el Pre-procesamiento: Rebalanceo y Aumento de Datos**

El objetivo aquí es corregir el dataset antes de que el modelo aprenda de él. Una técnica común es el "pesado de importancia" (importance weighting), que asigna mayor peso a las muestras de subgrupos subrepresentados para que su distribución en el entrenamiento coincida con la población real.7

Otra estrategia es el sobremuestreo sintético (SMOTE) enfocado en los límites de decisión (Borderline-SMOTE).32 En el diagnóstico de Alzheimer mediante imágenes de resonancia magnética (MRI), el uso de Borderline-SMOTE para equilibrar géneros y clases redujo la brecha en la puntuación F1 entre hombres y mujeres de un 7% a menos de un 3%, sin sacrificar la potencia predictiva general.32 Este enfoque es aplicable a clústeres socioeconómicos, asegurando que el modelo tenga suficientes ejemplos de pacientes de IDH bajo para aprender sus patrones específicos.

### **Mitigación en el Procesamiento: "Adversarial Debiasing"**

El "Adversarial Debiasing" es una técnica avanzada donde se entrenan dos redes simultáneamente: un predictor (que busca detectar la enfermedad) y un adversario (que intenta adivinar el atributo sensible, como el SES, a partir de las predicciones del primero).7 El objetivo del entrenamiento es maximizar la precisión del predictor mientras se minimiza la capacidad del adversario para identificar el perfil socioeconómico.30 Esto fuerza al modelo a aprender representaciones que son diagnósticamente útiles pero socioeconómicamente ciegas, eliminando "atajos" algorítmicos basados en la desigualdad.7

| Técnica de Mitigación | Mecanismo de Acción | Aplicación Sugerida |
| :---- | :---- | :---- |
| **F-MCCA** | Optimiza la correlación multimodal equilibrando los grupos demográficos. | Análisis conjunto de voz, imagen y metadatos clínicos. |
| **Constraint-Based Optimization** | Añade restricciones de equidad (como paridad demográfica) a la función de pérdida. | Modelos de soporte a la decisión clínica para evitar discriminación. |
| **Group DRO** | Minimiza el riesgo máximo entre diferentes grupos protegidos. | Mejora el rendimiento en los subgrupos con peores resultados (p.ej., SES muy bajo). |
| **Domain Alignment** | Alinea las distribuciones de datos de diferentes poblaciones (p.ej., etnias). | Transferencia de modelos entrenados en un país (HIC) a otro (LMIC). |

2

## **Evaluación del Performance bajo un Enfoque de Equidad**

Evaluar el rendimiento del modelo simplemente a través de la precisión global es insuficiente cuando se trabaja con datos socioeconómicos. Es necesario emplear métricas de equidad que desglosen el rendimiento por subgrupos.

1. **Igualdad de Oportunidades (Equal Opportunity):** Se cumple si el modelo tiene la misma sensibilidad (True Positive Rate) para todos los grupos socioeconómicos. Es vital en salud para asegurar que no se omitan casos de demencia en los sectores más pobres.32  
2. **Paridad Demográfica:** Exige que la tasa de predicción positiva sea igual para todos los grupos, independientemente de su IDH. Aunque puede ser controvertida si las prevalencias reales difieren, ayuda a cuestionar sesgos en la asignación de recursos.32  
3. **Error de Disparidad de Correlación:** En modelos multimodales, esta métrica mide si las relaciones aprendidas entre, por ejemplo, el habla y la atrofia cerebral, son consistentes a través de los niveles de riqueza.33

En el contexto de MultiConAD, las evaluaciones han demostrado que los adultos de más de 80 años y los hablantes de español a menudo presentan sensibilidades más bajas que los hablantes de inglés, lo que subraya la necesidad de auditorías constantes de performance estratificada por metadata demográfica y cultural.34

## **Casos de Uso y Aplicabilidad en el Contexto de Perú y Latinoamérica**

La integración de perfiles socioeconómicos es particularmente relevante en regiones con alta desigualdad como América Latina. En Perú, existen recursos estatales que pueden funcionar como metadata de entrada para potenciar la precisión de los modelos.

### **Aprovechamiento de ENDES e INEI**

La Encuesta Demográfica y de Salud Familiar (ENDES) del INEI proporciona datos actualizados sobre comorbilidades y factores de riesgo asociados al nivel de riqueza y educación.24 Un modelo de detección de Alzheimer en Perú podría beneficiarse de incluir el "Quintil de Bienestar" como variable de entrada. La evidencia de 2024 muestra que el exceso de peso y las comorbilidades varían significativamente según el nivel educativo y la autoidentificación étnica, factores que influyen en la trayectoria del envejecimiento cognitivo.24

Además, el INEI ha avanzado en la creación de mapas de "Pobreza a Nivel de Manzana" y "Vulnerabilidad Económica".36 Estos datos, revisados en 2025, permiten una vinculación geoespacial de alta resolución. Si un dataset clínico peruano incluye la manzana de residencia del paciente, es posible integrar un vector de vulnerabilidad que informe al modelo sobre factores ambientales que podrían estar afectando el rendimiento del paciente en tareas de descripción de imágenes o fluidez verbal.23

### **El Informe PNUD 2025 y el IDH Distrital**

El Informe sobre Desarrollo Humano 2025 del PNUD para Perú ofrece una base de datos en formato Excel con el IDH ajustado por desigualdad a nivel distrital para el periodo 2017-2024.38 Esta metadata permite:

* Crear **clústeres de IDH** para alimentar el modelo de IA, facilitando el aprendizaje de patrones regionales.  
* Calcular el **Índice de Densidad del Estado (IDE)**, que refleja la provisión de servicios públicos.22 Un IDE bajo en el distrito del paciente puede alertar al modelo sobre una posible falta de diagnósticos previos, permitiendo que el sistema de IA actúe como una herramienta de triaje más sensible en esas zonas.

## **Horizontes Tecnológicos: Modelos de Lenguaje y Gemelos Digitales**

El futuro del diagnóstico de demencia se dirige hacia el uso de modelos de lenguaje de gran escala (LLM) y la creación de "gemelos digitales" de pacientes.39 Estos sistemas integran datos longitudinales para predecir la progresión de MCI a Alzheimer con una precisión superior al 85% en entornos de investigación.40 Sin embargo, la implementación en el mundo real muestra tasas de falsos positivos entre un 15% y 23% mayores, en parte debido a la falta de ajuste a contextos socioeconómicos diversos.40

Las estrategias de adaptación para LLM, como el aprendizaje en contexto (In-Context Learning) con selección de demostraciones similares, han mostrado que el rendimiento en la detección de deterioro cognitivo mejora significativamente cuando se utilizan "prototipos" que coinciden con el perfil demográfico del paciente evaluado.39 Esto sugiere que, al alimentar un LLM con una pequeña descripción del perfil socioeconómico y educativo del paciente como parte del *prompt*, el modelo puede ajustar su razonamiento clínico de manera más equitativa.

## **Conclusiones y Recomendaciones Estratégicas**

La integración de indicadores socioeconómicos en los modelos de detección de enfermedades neurodegenerativas no es una opción secundaria, sino un componente central de la validación clínica moderna. La metadata asociada a los datasets existentes (como LASI-DAD y MultiConAD) y los índices georreferenciados (IDH, ADI, mapas de pobreza del INEI) ofrecen una oportunidad sin precedentes para robustecer estos sistemas.

Para avanzar en esta dirección, se recomienda:

1. **Enriquecer los datasets clínicos con medidas de área:** Utilizar técnicas de geocodificación para vincular los registros de los pacientes con el IDH distrital y otros índices de vulnerabilidad socioeconómica.  
2. **Adoptar un modelado consciente de la equidad:** Implementar técnicas de mitigación de sesgos como el Adversarial Debiasing y el sobremuestreo SMOTE para asegurar que el modelo no aprenda correlaciones espurias basadas en la pobreza o la falta de educación.  
3. **Auditar el performance por clústeres socioeconómicos:** Sustituir la métrica de precisión global por una evaluación detallada de la sensibilidad y especificidad en cada estrato socioeconómico, garantizando la "Igualdad de Oportunidades" en el diagnóstico.  
4. **Armonizar datos a nivel local:** En el caso peruano, utilizar las bases de datos de ENDES y los anexos del informe PNUD 2025 para crear vectores de entrada que reflejen la realidad epidemiológica y social del país.

Al integrar estas dimensiones, la IA no solo aumentará su precisión técnica, sino que se convertirá en una herramienta verdaderamente democratizadora, capaz de identificar signos tempranos de demencia con la misma eficacia tanto en entornos urbanos privilegiados como en comunidades rurales o vulnerables. El camino hacia una medicina de precisión equitativa requiere que los algoritmos entiendan no solo la biología del cerebro, sino también el tejido social en el que este envejece.

#### **Fuentes citadas**

1. Envisioning the Future of Machine Learning in the Early Detection of Neurodevelopmental and Neurodegenerative Disorders via Speech and Language Biomarkers \- MDPI, acceso: abril 3, 2026, [https://www.mdpi.com/2624-599X/7/4/72](https://www.mdpi.com/2624-599X/7/4/72)  
2. Advancing Fair and Explainable Machine Learning for Neuroimaging Dementia Pattern Classification in Multi-Ethnic Populations \- PubMed, acceso: abril 3, 2026, [https://pubmed.ncbi.nlm.nih.gov/40661475/](https://pubmed.ncbi.nlm.nih.gov/40661475/)  
3. Assessing the Impact of Sociodemographic Factors on Artificial Intelligence Models in Predicting Dementia: Retrospective Cohort Study \- PMC, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12912463/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12912463/)  
4. Machine Learning Approaches to Racial/Ethnic Differences in Social Determinants of Mild Cognitive Impairment and Its Progression to Dementia in the All of Us Research Program \- PMC, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12597675/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12597675/)  
5. Direct Effect of Life-Course Socioeconomic Status on Late-Life Cognition and Cognitive Decline in the Rush Memory and Aging Project \- PMC, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10505419/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10505419/)  
6. Socioeconomic status and the continuum of cognitive decline: A machine learning approach to identify critical windows for dementia onset \- UK Biobank, acceso: abril 3, 2026, [https://www.ukbiobank.ac.uk/projects/socioeconomic-status-and-the-continuum-of-cognitive-decline-a-machine-learning-approach-to-identify-critical-windows-for-dementia-onset/](https://www.ukbiobank.ac.uk/projects/socioeconomic-status-and-the-continuum-of-cognitive-decline-a-machine-learning-approach-to-identify-critical-windows-for-dementia-onset/)  
7. Algorithm fairness in artificial intelligence for medicine and healthcare \- PMC \- NIH, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10632090/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10632090/)  
8. Harmonized LASI-DAD Documentation, acceso: abril 3, 2026, [https://lasi-dad.org/codebooks/Harmonized%20LASI-DAD%20A.3.pdf](https://lasi-dad.org/codebooks/Harmonized%20LASI-DAD%20A.3.pdf)  
9. Harmonized LASI-DAD Documentation, acceso: abril 3, 2026, [https://lasi-dad.org/codebooks/Harmonized%20LASI-DAD%20B.1%202017-2024.pdf](https://lasi-dad.org/codebooks/Harmonized%20LASI-DAD%20B.1%202017-2024.pdf)  
10. LASI-DAD study: a protocol for a prospective cohort study of late-life cognition and dementia in India \- PMC, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6677961/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6677961/)  
11. Lifetime occupational skill and later‐life cognitive function among older adults in the United States, Mexico, India, and South Africa \- PMC, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10947921/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10947921/)  
12. Multi-modal data analysis for early detection of alzheimer's disease and related dementias, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12811763/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12811763/)  
13. Early Alzheimer's Detection via Speech AI | PDF | Deep Learning \- Scribd, acceso: abril 3, 2026, [https://www.scribd.com/document/981598528/Research-Proposal](https://www.scribd.com/document/981598528/Research-Proposal)  
14. MultiConAD: A Unified Multilingual Conversational Dataset for Early Alzheimer's Detection, acceso: abril 3, 2026, [https://www.researchgate.net/publication/389392424\_MultiConAD\_A\_Unified\_Multilingual\_Conversational\_Dataset\_for\_Early\_Alzheimer's\_Detection](https://www.researchgate.net/publication/389392424_MultiConAD_A_Unified_Multilingual_Conversational_Dataset_for_Early_Alzheimer's_Detection)  
15. Statistical analysis of interpretable linguistic features for MCI ..., acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12887683/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12887683/)  
16. DementiaBank English Pitt Corpus \- TalkBank, acceso: abril 3, 2026, [https://talkbank.org/dementia/access/English/Pitt.html](https://talkbank.org/dementia/access/English/Pitt.html)  
17. Tools for Analyzing Talk Part 1: The CHAT Transcription Format, acceso: abril 3, 2026, [https://reshare.ukdataservice.ac.uk/853329/22/CHAT\_TranscriptionGuidelines.pdf](https://reshare.ukdataservice.ac.uk/853329/22/CHAT_TranscriptionGuidelines.pdf)  
18. When and How to Use Area-Level Measures for Health Analysis: A Review and Recommendation Report, acceso: abril 3, 2026, [https://www150.statcan.gc.ca/n1/pub/11-633-x/11-633-x2026001-eng.htm](https://www150.statcan.gc.ca/n1/pub/11-633-x/11-633-x2026001-eng.htm)  
19. Link Your Large Health Data Sets to the Area Deprivation Index, the ezADI Way \- PMC, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12049168/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12049168/)  
20. PREDICTION MODEL OF HUMAN DEVELOPMENT INDEX (HDI) USING K-NEAREST NEIGHBOR (KNN) ENSEMBLE \- EJournal Universitas Nusa Mandiri, acceso: abril 3, 2026, [https://ejournal.nusamandiri.ac.id/index.php/jitk/article/download/6598/1455](https://ejournal.nusamandiri.ac.id/index.php/jitk/article/download/6598/1455)  
21. PNUD: Índice de Desarrollo Humano en el Perú aumentó en 2.16%, entre el 2017 y el 2024, acceso: abril 3, 2026, [https://elperuano.pe/noticia/273884-pnud-indice-de-desarrollo-humano-en-el-peru-aumento-en-216-entre-el-2017-y-el-2024](https://elperuano.pe/noticia/273884-pnud-indice-de-desarrollo-humano-en-el-peru-aumento-en-216-entre-el-2017-y-el-2024)  
22. Informe sobre Desarrollo Humano Perú 2025 \- United Nations ..., acceso: abril 3, 2026, [https://www.undp.org/sites/g/files/zskgke326/files/2025-07/informe\_sobre\_desarrollo\_humano\_pnud\_2025-version\_digital.pdf](https://www.undp.org/sites/g/files/zskgke326/files/2025-07/informe_sobre_desarrollo_humano_pnud_2025-version_digital.pdf)  
23. El uso de la tecnología para las políticas de combate a la pobreza: un mapa de pobreza y asentamientos irregulares de la Ciudad de México \- Centro Latam Digital, acceso: abril 3, 2026, [https://centrolatam.digital/publicacion2/el-uso-de-la-tecnologia-para-las-politicas-de-combate-a-la-pobreza-un-mapa-de-pobreza-y-asentamientos-irregulares-de-la-ciudad-de-mexico/](https://centrolatam.digital/publicacion2/el-uso-de-la-tecnologia-para-las-politicas-de-combate-a-la-pobreza-un-mapa-de-pobreza-y-asentamientos-irregulares-de-la-ciudad-de-mexico/)  
24. Perú: 2024 \- Instituto Nacional de Estadística e Informática \- INEI, acceso: abril 3, 2026, [https://www.inei.gob.pe/media/MenuRecursivo/publicaciones\_digitales/Est/Lib2017/libro.pdf](https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib2017/libro.pdf)  
25. Comparison of two area-level socioeconomic deprivation indices: Implications for public health research, practice, and policy | PLOS One, acceso: abril 3, 2026, [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0292281](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0292281)  
26. Digital Determinants of Health: Health data poverty amplifies existing health disparities—A scoping review \- PMC, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10569513/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10569513/)  
27. MultiConAD: A Unified Multilingual Conversational Dataset for Early Alzheimer's Detection | Request PDF \- ResearchGate, acceso: abril 3, 2026, [https://www.researchgate.net/publication/393657688\_MultiConAD\_A\_Unified\_Multilingual\_Conversational\_Dataset\_for\_Early\_Alzheimer's\_Detection](https://www.researchgate.net/publication/393657688_MultiConAD_A_Unified_Multilingual_Conversational_Dataset_for_Early_Alzheimer's_Detection)  
28. AI-Tool for Early-Stage Dementia Detection using Speech Analysis \- iarjset, acceso: abril 3, 2026, [https://iarjset.com/wp-content/uploads/2026/03/IARJSET.2026.13365-AI.pdf](https://iarjset.com/wp-content/uploads/2026/03/IARJSET.2026.13365-AI.pdf)  
29. Bias in Large AI Models for Medicine and Healthcare: Survey and Challenges \- Preprints.org, acceso: abril 3, 2026, [https://www.preprints.org/manuscript/202511.1838](https://www.preprints.org/manuscript/202511.1838)  
30. AI-Driven Healthcare: A Survey on Ensuring Fairness and Mitigating Bias \- arXiv, acceso: abril 3, 2026, [https://arxiv.org/html/2407.19655v1](https://arxiv.org/html/2407.19655v1)  
31. Understanding-informed Bias Mitigation for Fair CMR Segmentation \- Melba Journal, acceso: abril 3, 2026, [https://www.melba-journal.org/pdf/2025:036.pdf](https://www.melba-journal.org/pdf/2025:036.pdf)  
32. Comparative assessment of fairness definitions and bias mitigation strategies in machine learning-based diagnosis of Alzheimer's disease from MR images | Request PDF \- ResearchGate, acceso: abril 3, 2026, [https://www.researchgate.net/publication/398309375\_Comparative\_assessment\_of\_fairness\_definitions\_and\_bias\_mitigation\_strategies\_in\_machine\_learning-based\_diagnosis\_of\_Alzheimer's\_disease\_from\_MR\_images](https://www.researchgate.net/publication/398309375_Comparative_assessment_of_fairness_definitions_and_bias_mitigation_strategies_in_machine_learning-based_diagnosis_of_Alzheimer's_disease_from_MR_images)  
33. Fair Multi-modal Canonical Correlation Analysis: A Neuroimaging Study of Alzheimer's Disease \- PMC, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12919458/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12919458/)  
34. (PDF) An automatic Alzheimer's disease classifier based on reading task for Spanish language \- ResearchGate, acceso: abril 3, 2026, [https://www.researchgate.net/publication/386739663\_An\_automatic\_Alzheimer's\_disease\_classifier\_based\_on\_reading\_task\_for\_Spanish\_language](https://www.researchgate.net/publication/386739663_An_automatic_Alzheimer's_disease_classifier_based_on_reading_task_for_Spanish_language)  
35. Perú: Encuesta Demográfica y de Salud Familiar, Endes 2024 \- Informes y publicaciones, acceso: abril 3, 2026, [https://www.gob.pe/institucion/inei/informes-publicaciones/6813623-peru-encuesta-demografica-y-de-salud-familiar-endes-2024](https://www.gob.pe/institucion/inei/informes-publicaciones/6813623-peru-encuesta-demografica-y-de-salud-familiar-endes-2024)  
36. Pobreza Multidimensional \- Avance (Revisión 2025), acceso: abril 3, 2026, [https://www.gob.pe/institucion/inei/informes-publicaciones/6524650-pobreza-multidimensional-avance-revision-2025](https://www.gob.pe/institucion/inei/informes-publicaciones/6524650-pobreza-multidimensional-avance-revision-2025)  
37. Cifras de Pobreza \- Compendios \- Instituto Nacional de Estadística e Informática \- Plataforma del Estado Peruano, acceso: abril 3, 2026, [https://www.gob.pe/institucion/inei/colecciones/27283-cifras-de-pobreza](https://www.gob.pe/institucion/inei/colecciones/27283-cifras-de-pobreza)  
38. Informe sobre Desarrollo Humano 2025 \- Actuar, confiar y conectar caminos, acceso: abril 3, 2026, [https://www.undp.org/es/peru/publicaciones/informe-sobre-desarrollo-humano-2025-actuar-confiar-y-conectar-caminos](https://www.undp.org/es/peru/publicaciones/informe-sobre-desarrollo-humano-2025-actuar-confiar-y-conectar-caminos)  
39. Large Language Model Adaptation Strategies in Speech-Based Cognitive Screening: Systematic Evaluation \- JMIR AI, acceso: abril 3, 2026, [https://ai.jmir.org/2026/1/e82608](https://ai.jmir.org/2026/1/e82608)  
40. Digital Twin Cognition: AI-Biomarker Integration in Biomimetic Neuropsychology \- PMC, acceso: abril 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12561581/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12561581/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAsCAYAAADYUuRgAAALY0lEQVR4Xu2dC6hmVRXHV/R+0buMXmOYEWlCWaRlhlRklISalSUNGJphIimVMtm1kh5kaohIiWIig2ZZVPQkPgrUHjQ2WEkq3cQHFSWIBhk99s+9V2fPme+713tn7mNmfj9Y3P3tvc85e+8zcv6utR8RIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiezj7FDu62F7jglXmYVHb8bZxwQqzFv0/pdhzx5kiIiIiC3FJsSeOM9eAHxe7cpy5Cqxm/48qdtg4cwqPKXZtsSeMC0RERGTP4ynFfjnOXCPuLnbiOHOFWc3+P77Yl8aZIiIisudxQrFvFXtSsVOL3dSVndV+byx2est7T7G/ZYXCw4sdU2y+2I0tDw/Un4q9K+r1B7b8BC8QdT4Ytfy3XdnZxX5R7NKobYJp7QCue3r3e6kQVl2s/z+P+tz0XE3r//VR+/+mlndDsS3Fzi12Wwz9SLjXnVGft7nYrcUOL7ahpdOjtrXYX1oabo46Nse3v19p+fTjlqj9gEcUuyOq2MNuL3ZSS3OP49o1ycXF/lDsoi5PRERE1hEfjipAmAuGQLm35SMyNkUVJIgDhAcgtH7W0nBFMzik2CuKvTOqyDkjqlj7aCtPKMf+G7X8npb/kqjX8Mwzo7ZpVjvwPhEO7YXHUnljLN7/p0V97rNa/rT+0xa4q9iriu0bNTx5cLHToo5JT47PA8We2vIQVV9oaUK93PM5UYUf0B7GByH81qj95nlAP5hbh8cRDip2aLH7o4pARCZjnPPgGMPszxuawdVRxZ6IiIisM5j7dE3UDzXzsvDCIAx6L9J8VGEDCJojW3rvYhfGIJq4DnHGfXpRMw3qIH4SRMN/in0zqmfpNS1/VjvwSL1yKPo/xxabLGBjFus/omm+pWFa/xOuof+0674ufxqTYpe1dD8WhFxpA+CJm7Q0HBGDoIR+bL4b1VuXcO9JSyNsEYFAP6lLv+diEMvAc5/d/RYREZF1AuIEDwzsV+wTUb1NeL8SPuqvbWlEAtcA9VK8APdBVIwF3zT65wJC7F/d72RWO86JHQuHJov1n+f1omah/nMN/WdeXXq7ZsF98rl9G/COvbmlx4INQZXz5xBe3+/KuB8h6IRwMWM0TiMyT27pSWwrrLm3ixZERETWIXi2MmT38ahCANGQgoNQGx6ZFxR7RrHLi70wqlftpTGIC1Yz5jW9sJgFdfAmJbThz93vDIlOaweig9AgYupDrXy5LNZ/5nbx3Ati8f4TDoVeIM2C8cn+92MxiRqGxXM3Fmy0KYUdY4PQI7xK+JT6XJfz5ahLO8dp2o9H77xi58cg+rjuyy0tIiKyqjDv6ZlRwzyY3oPpPDnqx34MeQgTxi3Hjrr9OBJaG4fR+Pg/cpQ3JoXFGO7FM3qmtYPfPHtnsFD/oe/vtP6P/10hvjJMPIt+fPqxWKhf4zHr20y6v25WGvr28jz+G+G/FRERkTWBj/+5UUNVvyr2um2LRURERGQ9gHdhPurkcRERERFZhzB3J1fFiYiIiMg6hMnruc9Ugnhjr6zVgtBs7oH1UGCOERPAZ9l4zpSIiIjILgvCDO/aOBzK6jq2XoAfxLB56c6ClYbv635/L5Z+SHkulBjbQnxG09bAHh0iIiI7QG7G2sMO72zHwB5erNTL1XqslCONKOJv7gQPudqUFXWkEYLj1YGU56q9fpVjXstf8rG+7izGQq23xVYgioiIiOwyEA7tBRuetf2LfS2qcPpIDDvnn1bsuqieMPJfVuzFrWxz1L26OAII46iik2LYwwqB9+piH2vlJ8Yg+K4q9paoxw69P+o1tOGaVj4NQ6IiIiKy24P36kdRt/PAPtfyr4/qGUOwAQIuNyz9atSNWBFbsF/Ufa8QahuLvajlQ25eyiakgGBj09fftN95tBBHFOHJ476IPP7yHMRcv0v9WnNAsaNj+32+VhrGDWG8u8Jmv4zrXuOCFeSUWNp8SRERkXXHD6OuGuXvy6Me0YP3izlunLXI30tbXc6EpAyPWXq0EFqkEXGEJY8t9vxiP4m6e3wvxt4eVaBR/+yoHjzuibE7PmJvvYgVjmP6Y+yco56WArv0Hz/OnAHjjQhfLJS8nkA8sf9fHmW10jBG/y72+lH+NPj3uZoLb0RERB4yOfcr5631c8EyL7f/6Ms4+mfaNY/r8vqd6x/VpXuvFfl5PfdcLyBi7x5nrjDM6Tt4nLmbgfd2sSO6dhb8e0rProiIiOwCnFDslqhi8dRiN3VlZ7XfG4ud3vLOiXr+ZYKYOibqhsM3tjzm3W2JenLEbbF9+JTyG6KGgX9a7I5izyt2eEt/Z6j6oGgl//dRPY/pgXps1LM7ETlzLc1z+v4AHkHuSagRkXJ71DmFmT6u1QPCgxe3/Iu6/OWAZ5TQNueZMteRNkDfH84jzf4QOudQ9p5vFLs16ntA5F8S9VxUDm7nvRw4VH0QPLR3Rn2PzKXkWp61oaUPa/U4xP2uVh94F7ynaeO/NWo/gBXNlDN247G8OepY9v+Twtmt1OkPjRcREZFlwEIKVsIiKhAG97Z8BM+mqIKMDzYfdCAcfGVLwxXN4JCoh5qzaOLaqF4xRBZh4R7KCbEhGrg/3iUWcfDBJ9TaC0IWdSDqEALMMURUIBwQjoDQeUcMz6E/zAfLrVG4/tCo26VsaPXviSrOmIOY/QJEH6uFEUdXR33OcmA8Px+1H4S13x01/Ah9fz4VtT+AGOuFzcYYxBzjz30IC5N/RlSxRl5Plj8Qw/YzCCbGG3h3eNewb0cVbPSRcPuk2AdiW08f/SBsn78PijqW98f2YwmMJfUBgTzX0u+NKshFRERkmeT+c3y4mVuHtwSh0Ht75mNYIXtfVM8Y7F3swhi8KlyXIoJ6C4G4OqKluV8KF+byIQiAtiF6EHE8IwVH0rd9Vh7XXRaDNwmxyX2A1bfUhbmoi0cSxqHfy445iJMFbBoInTzcHW/juD+0K/uDUD6ypWk7HriENk6ivp/FvFWTqPcF6iMEgXb0YdDLYxgT3kUK9X78gWvwwCXce9LS/VjSZtpJHxF2/2z5gAhOAS0iIiLLoBdnCBZCiHxc8WYleFH4kEMKDqBeigzA45IibLF5bni3mA83Ts/FIFYQTIgCxA2CI71qCQs/5kd59KEXm2OPHem8D+G9k6MKl0lUgQPpZUpBsxx4bj4Hr9MXY/v+9HPWaHN61LJewlgilMZCehqU58pk6mcaEUWYNukFG+Of72suthWLpMlL+vHr04h3xhIQ7f9oaaDO2MsqIiIiSwDvx99bmjlVeEr4uOcHfJ+onhPmYvFR5mOc4o2QWYqAo2K4phcr0+hF1FhQ0RbaROiQsOyZLR9PEc/7ZFRvX27BwpwtSOGIxwevH8b1vRgB0ikO6Rcijd/nR50XB9yDPex2BMRSepU+G1UcjfuDuKI/hJERULQDMUc7aD8w7owF+Xi7epE3jfTqAfUzPYm6ajbv2ws2rsn31Y8/sIqZdvPuoR+/Ps39GMvzoq6WJtwN3KcXgCIiIrIM+GhvjvphzXlPzOFCDH066j50zO3C44OYY5sT6gMiggn+OS9r35Z/QGx/JmsP5X9taTwvKRjh11GFRi4a2BpVSLKlB14m5obhxWPbjguKfT2qSGD+HSC8aCNzvABhlGFPyLAdMDeMRQbAnCv6xbOYD8cY7AiMFYswuBeiN+n7c1PU/lB3SwzjClzLO/hdDCFnhGQf1hxDeDXL02uYMC6MH+NyXdQ5ddx7/6jvIt8X4U/Eao4/7coQK/Tj16eZ/8ZYsgUIY7cpat+vitXdW05ERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERkD+F/Djd94lSs9REAAAAASUVORK5CYII=>