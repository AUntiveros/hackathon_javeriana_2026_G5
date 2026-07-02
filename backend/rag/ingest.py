"""Ingesta del Personal Knowledge Graph (PKG) a ChromaDB.

Prototipo de RAG. Carga los nodos del PKG de Don José como documentos con embeddings.
Embeddings: Gemini text-embedding-004 si hay GEMINI_API_KEY; si no, sentence-transformers local.

Uso:
    python -m backend.rag.ingest
"""
import json
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

SEED_PATH = Path(__file__).resolve().parents[1] / "seed" / "don_jose.json"
CHROMA_PATH = Path(__file__).resolve().parents[1] / "chroma_db"
COLLECTION = "pkg_don_jose"


def get_embedder():
    """Devuelve una función embed(list[str]) -> list[list[float]]."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = os.environ.get("GEMINI_EMBED_MODEL", "text-embedding-004")

        def embed(texts):
            out = []
            for t in texts:
                r = genai.embed_content(model=model, content=t, task_type="retrieval_document")
                out.append(r["embedding"])
            return out

        print("[embedder] Gemini text-embedding-004")
        return embed

    # Fallback offline
    from sentence_transformers import SentenceTransformer

    st = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    print("[embedder] sentence-transformers (offline)")
    return lambda texts: st.encode(texts, normalize_embeddings=True).tolist()


def node_to_document(node: dict) -> str:
    """Convierte un nodo del PKG en un texto recuperable."""
    rel = node.get("relacion_paciente", "")
    rel_txt = f" ({rel} del paciente)" if rel else ""
    return f"[{node['tipo']}] {node['nombre']}{rel_txt}: {node['atributos']}"


def main():
    data = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    nodes = data["pkg_nodes"]

    docs = [node_to_document(n) for n in nodes]
    ids = [n["id"] for n in nodes]
    metas = [{"tipo": n["tipo"], "nombre": n["nombre"]} for n in nodes]

    embed = get_embedder()
    embeddings = embed(docs)

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.create_collection(COLLECTION)
    col.add(ids=ids, documents=docs, embeddings=embeddings, metadatas=metas)

    print(f"[ingest] {len(docs)} nodos del PKG cargados en '{COLLECTION}'")


if __name__ == "__main__":
    main()
