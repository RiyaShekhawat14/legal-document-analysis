import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim=384):
        self.index = faiss.IndexFlatL2(dim)
        self.text_chunks = []

    def add_embeddings(self, embeddings, chunks):
        embeddings_array = np.array(embeddings).astype("float32")
        self.index.add(embeddings_array)
        self.text_chunks.extend(chunks)

    def search(self, query_embedding, k=3):
        query = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query, k)

        results = []

        for idx in indices[0]:
            if idx == -1:
                continue
            if idx < len(self.text_chunks):
                results.append(self.text_chunks[idx])

        return results