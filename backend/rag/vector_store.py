from __future__ import annotations

import atexit
from pathlib import Path
from uuid import uuid4

import numpy as np

from config.settings import settings
from utils.logger import logger

try:
    import faiss
except ImportError:
    faiss = None
    logger.warning("faiss is not installed. FAISS backend will be unavailable if selected.")

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams
except Exception:
    QdrantClient = None
    Distance = None
    PointStruct = None
    VectorParams = None


class VectorStore:
    def __init__(self, dim: int = 384, collection_name: str | None = None):
        self.dim = dim
        requested_backend = settings.VECTOR_DB_BACKEND.lower()
        self.backend = "qdrant" if requested_backend == "qdrant" else "faiss"
        self.text_chunks: list[str] = []
        self._faiss_index = None
        self._qdrant_client = None
        self._embeddings = None
        self._collection_name = collection_name or settings.VECTOR_DB_COLLECTION
        self._storage_path = str(Path(settings.VECTOR_DB_PATH).resolve())

        if self.backend == "faiss":
            if faiss is None:
                logger.warning(
                    "Requested FAISS backend, but faiss is unavailable. Falling back to Qdrant backend."
                )
                self.backend = "qdrant"
            else:
                self._faiss_index = faiss.IndexFlatL2(dim)

        if self.backend == "qdrant":
            self._init_qdrant()
            if self._qdrant_client is None:
                if faiss is not None:
                    logger.warning(
                        "Qdrant backend unavailable. Falling back to FAISS backend."
                    )
                    self.backend = "faiss"
                    self._faiss_index = faiss.IndexFlatL2(dim)
                else:
                    logger.warning(
                        "Qdrant backend unavailable and faiss is not installed. Using in-memory fallback."
                    )
                    self.backend = "memory"

    def _init_qdrant(self):
        if QdrantClient is None:
            logger.warning(
                "qdrant-client is not installed. Falling back to in-memory FAISS vector search."
            )
            self.backend = "faiss"
            return

        try:
            storage_path = Path(self._storage_path)
            storage_path.mkdir(parents=True, exist_ok=True)
            self._qdrant_client = QdrantClient(path=str(storage_path))
            atexit.register(self.close)
            self._ensure_collection(reset=False)
        except Exception as exc:
            logger.warning(
                "Qdrant local store could not be initialized (%s). Falling back to FAISS.",
                exc,
            )
            self._qdrant_client = None
            self.backend = "faiss"

    def _ensure_collection(self, reset: bool):
        if self.backend != "qdrant" or self._qdrant_client is None:
            return

        exists = self._qdrant_client.collection_exists(self._collection_name)

        if exists and reset:
            self._qdrant_client.delete_collection(self._collection_name)
            exists = False

        if not exists:
            self._qdrant_client.create_collection(
                collection_name=self._collection_name,
                vectors_config=VectorParams(
                    size=self.dim,
                    distance=Distance.COSINE,
                ),
            )

    def reset(self):
        self.text_chunks = []
        self._embeddings = None

        if self.backend == "qdrant":
            self._ensure_collection(reset=True)
        elif self._faiss_index is not None:
            self._faiss_index = faiss.IndexFlatL2(self.dim)

    def add_embeddings(self, embeddings, chunks):
        embeddings_array = np.asarray(embeddings, dtype="float32").reshape(-1, self.dim)
        self.text_chunks = list(chunks)

        if self.backend == "qdrant" and self._qdrant_client is not None:
            self._ensure_collection(reset=True)
            points = [
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding.tolist(),
                    payload={
                        "chunk": chunk,
                        "chunk_index": index,
                    },
                )
                for index, (embedding, chunk) in enumerate(zip(embeddings_array, chunks))
            ]
            if points:
                self._qdrant_client.upsert(
                    collection_name=self._collection_name,
                    points=points,
                )
            return

        if self.backend in {"qdrant", "memory"}:
            logger.warning(
                "No persistent vector backend available; storing embeddings in memory for fallback search."
            )
            self._embeddings = embeddings_array
            return

        if self._faiss_index is None:
            raise RuntimeError(
                "No available vector backend. Install faiss or qdrant-client, or configure a supported backend."
            )

        self._faiss_index.add(embeddings_array)

    def search(self, query_embedding, k: int = 3):
        if self.backend == "qdrant" and self._qdrant_client is not None:
            vector = np.asarray(query_embedding, dtype="float32").tolist()
            if hasattr(self._qdrant_client, "query_points"):
                response = self._qdrant_client.query_points(
                    collection_name=self._collection_name,
                    query=vector,
                    limit=k,
                    with_payload=True,
                )
                results = getattr(response, "points", response)
            else:
                results = self._qdrant_client.search(
                    collection_name=self._collection_name,
                    query_vector=vector,
                    limit=k,
                    with_payload=True,
                )
            return [
                point.payload["chunk"]
                for point in results
                if point.payload and point.payload.get("chunk")
            ]

        if (self.backend == "qdrant" and self._qdrant_client is None) or self.backend == "memory":
            if self._embeddings is None or self._embeddings.size == 0:
                return []
            query = np.asarray(query_embedding, dtype="float32").reshape(1, self.dim)
            distances = np.linalg.norm(self._embeddings - query, axis=1)
            best_indices = np.argsort(distances)[:k]
            return [
                self.text_chunks[idx]
                for idx in best_indices
                if idx != -1 and idx < len(self.text_chunks)
            ]

        if self._faiss_index is None or self._faiss_index.ntotal == 0:
            return []

        query = np.asarray([query_embedding], dtype="float32").reshape(1, self.dim)
        distances, indices = self._faiss_index.search(query, k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            if idx < len(self.text_chunks):
                results.append(self.text_chunks[idx])

        return results

    def get_status(self):
        if self.backend == "qdrant" and self._qdrant_client is not None:
            count = self._qdrant_client.count(
                collection_name=self._collection_name,
                exact=True,
            ).count
            return {
                "backend": "qdrant",
                "collection": self._collection_name,
                "path": self._storage_path,
                "vector_count": count,
                "distance": "cosine",
                "persistent": True,
            }

        return {
            "backend": "faiss",
            "collection": None,
            "path": None,
            "vector_count": int(self._faiss_index.ntotal),
            "distance": "l2",
            "persistent": False,
        }

    def close(self):
        if self._qdrant_client is None:
            return

        try:
            self._qdrant_client.close()
        except Exception:
            pass
