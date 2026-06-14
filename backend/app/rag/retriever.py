from app.rag.chunker import split_document
from app.rag.embeddings import (
    embed_documents,
    embed_query,
)

from app.db.vector_store import VectorStore


class CVRetriever:

    def __init__(self):

        self.store = None

    def index_cv(self, text):

        chunks = split_document(text)

        embeddings = embed_documents(chunks)

        self.store = VectorStore(
            embeddings.shape[1]
        )

        self.store.add(
            embeddings,
            chunks,
        )

    def retrieve(
        self,
        query,
        top_k=5,
    ):

        embedding = embed_query(query)

        return self.store.search(
            embedding,
            top_k,
        )