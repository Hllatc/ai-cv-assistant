import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension):

        self.index = faiss.IndexFlatIP(dimension)

        self.documents = []

    def add(self, embeddings, chunks):

        self.index.add(
            np.array(
                embeddings,
                dtype="float32"
            )
        )

        self.documents.extend(chunks)

    def search(self, embedding, k=5):

        scores, indices = self.index.search(
            np.array([embedding], dtype="float32"),
            k,
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            results.append({
                "score": float(score),
                "text": self.documents[idx]
            })

        return results