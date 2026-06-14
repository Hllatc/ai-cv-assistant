from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

def embed_documents(chunks):
    return model.encode(
        chunks,
        normalize_embeddings=True
    )

def embed_query(query):
    return model.encode(
        query,
        normalize_embeddings=True
    )