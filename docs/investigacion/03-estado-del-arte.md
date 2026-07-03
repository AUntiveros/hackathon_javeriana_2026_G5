# Estado del arte comparado — recordatorios de rutina para demencia

> Deliverable obligatorio · Fecha: 2026-07-03
> Foco delimitado: **recordatorio de una actividad cotidiana + confirmación + aviso al cuidador**.
> Cada fila: qué hace · qué tiene bueno · qué le falta · qué usamos de él para Nino.

---

## A) Productos comerciales

| Producto | Qué hace | Bueno | Le falta | Qué usamos |
|---|---|---|---|---|
| **Ato** (Argentina, J. Cereigido) · [link](https://www.iprofesional.com/tecnologia/441087) · [origen](https://empre.ar/podcast/un-nieto-una-idea-y-una-ia-asi-nacio-ato-el-asistente-virtual-pensado-para-su-abuelo/) | Asistente de **voz sin pantallas ni botones** para adultos mayores: recuerda medicación, mensajes a familia, conversación cotidiana | **Voz-primero** (valida nuestra tesis para analfabetos), cálido, comercial (US/ES/MX/AR), respaldo de inversión | No específico para demencia; sin **motor de criticidad**; sin confirmación estructurada + escalado al cuidador; sin offline/edge explícito; sin twin evolutivo | El modelo **voz-only sin fricción**; el "compañero que conversa". Nos diferenciamos con criticidad + confirmación + RBAC |
| **Reminder Rosie** (SMPL) · [link](https://reminder-rosie.com/) | Reloj-despertador **por voz**: hasta 25 recordatorios grabados con la **voz de un familiar**, manos libres, para demencia | Voz familiar aumenta adherencia; cero fricción; barato; sin pantalla | **No confirma** si se hizo; **no avisa al cuidador**; no adaptativo; no conversa; hardware fijo | La idea de **voz familiar** (calidez) y el hands-free. Añadimos el loop de confirmación + alerta |
| **MedMinder** · [link](https://www.medminder.com/) | **Pastillero inteligente** con modem celular: avisa al cuidador si no se toma la medicación tras varios avisos; compartimentos con llave; alerta de emergencia | **Confirma y escala al cuidador** (lo más cercano a la delimitación); comprobado | Solo pastillas; **hardware que bloquea** (contrario a autonomía); no conversa; caro; nube-dependiente | El patrón **avisos → confirmación → escalado**. Lo hacemos software + multi-actividad + respetando autonomía |
| **Alexa / Google Assistant** (recordatorios) | Recordatorios y rutinas genéricas por voz | Ubicuo, voz natural, ecosistema | No específico demencia; **no confirma cumplimiento**; no notifica al cuidador; nube obligatoria; asume usuario competente | Referencia de UX de voz. Nino aporta la capa de cuidado + offline + criticidad |

## B) Prototipos / investigación

| Trabajo | Qué hace | Bueno | Le falta | Qué usamos |
|---|---|---|---|---|
| **Caregiver-in-the-Loop AI Task Verification** (arXiv 2508.18267) · [link](https://arxiv.org/pdf/2508.18267) | IA generativa en recordatorios que **integra feedback del cuidador** en el proceso; verificación de tareas | Cierra el loop cuidador↔IA (gap señalado en la literatura) | Prototipo; sin criticidad diferenciada ni offline | El **loop cuidador-en-la-vuelta** para verificación de la actividad |
| **Remindful** (arXiv 2604.19574) · [link](https://arxiv.org/pdf/2604.19574) | Diseño de sistemas de recordatorio **interpretables por el cuidador** en demencia | Enfatiza el rol del cuidador en el diseño (gap frecuente) | Conceptual | Principios de diseño centrados en el cuidador |
| **Home-based reminder + ML de rutina** (2025) | Unidades de recordatorio + base central; el cuidador manda recordatorios por app, las unidades **detectan reconocimiento (acknowledgment)**; ML aprende horarios y detecta desviaciones | Detección de **acknowledgment** + desvíos de rutina; monitoreo remoto | Requiere hardware fijo en casa; no portátil/voz-first | La idea de **detectar reconocimiento** de la tarea + aprender la rutina (nuestro twin de jornada) |
| **SmartPrompt** (ClinicalTrials NCT04313582) · [link](https://clinicaltrials.gov/study/NCT04313582) | Prompts para mejorar función cotidiana en demencia; ensayo de factibilidad | Base de evidencia clínica de "prompting" para AVD | Investigación, no producto | Respaldo de evidencia: prompting cotidiano ayuda sin diagnosticar |
| **INTERDEM Assistive Tech Delphi** (Alzheimer's & Dementia 2025) · [link](https://alz-journals.onlinelibrary.wiley.com/doi/10.1002/alz.70755) | Recomendaciones de expertos para tecnología de apoyo en demencia | Marco de usabilidad/implementación/costo | — | Checklist de diseño responsable para el pitch |

---

## Síntesis — el hueco que llena Nino

Ningún producto ni prototipo combina las **cinco** cosas a la vez:

1. **Recordatorio por voz sin fricción** (como Ato/Rosie) …
2. **+ confirmación de cumplimiento + escalado al cuidador** (como MedMinder) …
3. **+ motor de criticidad con lógica difusa** que respeta la autonomía (**NADIE** lo hace: fuerzan todo o no confirman) …
4. **+ offline-first / edge** para la realidad rural LATAM (nadie: todos nube-dependientes) …
5. **+ contexto LATAM** (voz en español, baja escolaridad, hipertensión, ubicación por desorientación).

> **Frase de posicionamiento:** *"Ato y Rosie recuerdan; MedMinder confirma pero encierra; Nino
> recuerda, confirma y avisa —sin forzar—, decidiendo con lógica difusa qué es crítico y qué puede
> soltar, y funcionando aunque no haya internet."*

### Fuentes
- Ato: https://www.iprofesional.com/tecnologia/441087 · https://empre.ar/podcast/un-nieto-una-idea-y-una-ia-asi-nacio-ato-el-asistente-virtual-pensado-para-su-abuelo/
- Reminder Rosie: https://reminder-rosie.com/
- MedMinder: https://www.medminder.com/
- Caregiver-in-the-Loop: https://arxiv.org/pdf/2508.18267
- Remindful: https://arxiv.org/pdf/2604.19574
- SmartPrompt: https://clinicaltrials.gov/study/NCT04313582
- INTERDEM Delphi: https://alz-journals.onlinelibrary.wiley.com/doi/10.1002/alz.70755
- Home reminder + memoria/autonomía: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11711975/
