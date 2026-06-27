import uuid
from app.db.vector_store import client
from app.services.chunk_service import split_text

import requests
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(url="http://qdrant:6333")


def init_qdrant():
    if not client.collection_exists("cv"):
        client.create_collection(
            collection_name="cv",
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )
        

def get_embedding(text: str):
    response = requests.post(
        "http://ollama:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    data = response.json()

    print("OLLAMA RAW RESPONSE:", data)  # 🔥 KRİTİK DEBUG

    return data["embedding"]


def store_cv_chunks(user_id, text):
    chunks = split_text(text)

    points = []

    for i, chunk in enumerate(chunks):
        vector = get_embedding(chunk)  # 🔥 Ollama embedding

        points.append({
            "id": i,
            "vector": vector,
            "payload": {
                "user_id": user_id,
                "text": chunk
            }
        })

    client.upsert(
        collection_name="cv",
        points=points
    )

    return len(points)