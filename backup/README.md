# Backup — módulos descartados tras el pivote (2026-07-03)

El hackathon delimitó el problema a **recordatorios de rutina** y **prohibió** detectar/monitorear
deterioro cognitivo y el prototipo de cámara. Lo que quedó fuera se guardó aquí (recuperable), no se
borró.

| Carpeta/archivo | Qué era | Por qué se descartó | ¿Rescatable? |
|---|---|---|---|
| `ml-biomarcadores-descartado/` | Pipeline de biomarcadores de voz para detección de deterioro (P(AD\|Voz,SES), fairness, model.pkl) | Prohibido diagnosticar/evaluar progresión cognitiva | Concepto de fairness/SES sí es reutilizable como personalización (no como detección) |
| `uno_q-vision-camara-descartado/` | Asistente Uno Q con visión: objetos "¿qué es esto?", memoria espacial, reconocimiento facial | Prohibido el prototipo de cámara | El edge-LLM/voz/offline se re-especifica en el nuevo plan; el `hardware/bridge.py` de biométricos se reaprovecha para el smartwatch |
| `PROMPT-entrenamiento-biomarcadores.md` | Prompt para entrenar el modelo de detección | Ligado a biomarcadores descartados | No |
| `uno-q-vision-design.md` | Diseño del módulo de visión | Cámara descartada | Ideas de edge/offline sí |

**Nota:** el firmware de biométricos (`hardware/unoq_mcu/`, `hardware/esp32/`) NO está aquí —
se **reaprovecha** para el smartwatch (PPG: FC/variabilidad + presión estimada), que sí está
permitido porque no evalúa deterioro cognitivo (monitoreo cardiovascular en hipertensos).
