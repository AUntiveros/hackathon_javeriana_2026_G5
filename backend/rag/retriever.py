"""Recuperación desde el PKG en ChromaDB.

Uso como módulo:
    from backend.rag.retriever import query
    print(query("¿quién es Sofía?", k=3))

Prueba rápida por CLI:
    python -m backend.rag.retriever "¿dónde está mi sombrero?"
"""
import os
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

CHROMA_PATH = Path(__file__).resolve().parents[1] / "chroma_db"
COLLECTION = "pkg_don_jose"


def _embed_query(text: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = os.environ.get("GEMINI_EMBED_MODEL", "text-embedding-004")
        r = genai.embed_content(model=model, content=text, task_type="retrieval_query")
        return r["embedding"]
    from sentence_transformers import SentenceTransformer

    st = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return st.encode([text], normalize_embeddings=True).tolist()[0]


def query(text: str, k: int = 3) -> list[str]:
    """Devuelve los k fragmentos del PKG más relevantes a la consulta."""
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    col = client.get_collection(COLLECTION)
    res = col.query(query_embeddings=[_embed_query(text)], n_results=k)
    return res["documents"][0]


def context_block(text: str, k: int = 3) -> str:
    """Contexto formateado para inyectar en el prompt del agente."""
    docs = query(text, k)
    return "Contexto del paciente (memoria):\n" + "\n".join(f"- {d}" for d in docs)


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "¿quién es Sofía?"
    for d in query(q):
        print(" •", d)
