from qdrant_client import QdrantClient

client = QdrantClient(host="qdrant", port=6333)

def init_qdrant():
    client.recreate_collection(
        collection_name="cv_chunks",
        vectors_config={
            "size": 384,
            "distance": "Cosine"
        }
    )