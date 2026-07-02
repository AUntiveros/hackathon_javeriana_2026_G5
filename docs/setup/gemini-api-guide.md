# Guía de API key Gemini

LLM elegido para el orquestador + los 5 agentes de rol: **Gemini 2.5 Flash** (matchea el blueprint del paper Electronics 2026, tier gratis suficiente para la demo).

## 1. Obtener la API key (gratis)

1. Ir a **https://aistudio.google.com/apikey** (Google AI Studio).
2. Login con cuenta Google.
3. "Create API key" → copiar la clave (`AIza...`).
4. El tier gratis de AI Studio da cuota diaria suficiente para una hackathon (rate limits por minuto; si topa, esperar o crear segunda key).

## 2. Configurar en el proyecto

Crear `backend/.env` (NUNCA commitear — va en `.gitignore`):

```
GEMINI_API_KEY=AIza_tu_clave_aqui
GEMINI_MODEL=gemini-2.5-flash
GEMINI_EMBED_MODEL=text-embedding-004
```

`.gitignore` debe incluir:
```
.env
*.pkl
__pycache__/
node_modules/
```

## 3. Instalación

```bash
pip install google-generativeai langchain langchain-google-genai langgraph python-dotenv
```

## 4. Smoke test

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv("backend/.env")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")
print(model.generate_content("Responde solo: OK").text)
```

## 5. Notas de límites (tier gratis, verificar al día del evento)

- Gemini 2.5 Flash free: rate limit por minuto (RPM) y por día (RPD) acotados. Suficiente para demo; NO para carga real.
- Embeddings `text-embedding-004`: también gratis. Alternativa offline: `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`) si falla la red.
- Fallback de LLM si Gemini cae: `sentence-transformers` para RAG local + respuestas plantilladas, o cambiar a otra key. Tener la alternativa lista evita depender de conectividad en vivo.

## 6. Seguridad

- La key nunca en frontend ni en el repo. Solo backend, vía `.env`.
- Si se filtra, revocar en AI Studio y generar otra.
