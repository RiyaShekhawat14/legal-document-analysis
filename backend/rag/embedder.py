import hashlib

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None


MODEL_NAME = "all-MiniLM-L6-v2"
FALLBACK_DIM = 384
_model = None
_using_fallback = False


def _hashing_embedding(text: str, dim: int = FALLBACK_DIM):
    vector = np.zeros(dim, dtype="float32")

    for token in text.lower().split():
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dim
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    norm = np.linalg.norm(vector)
    if norm:
        vector /= norm

    return vector


def _load_model():
    global _model, _using_fallback

    if _model is not None or _using_fallback:
        return _model

    if SentenceTransformer is None:
        _using_fallback = True
        return None

    try:
        _model = SentenceTransformer(MODEL_NAME, local_files_only=True)
    except Exception:
        _using_fallback = True
        _model = None

    return _model


def get_embedding(text: str):
    text = text or ""
    model = _load_model()

    if model is None:
        return _hashing_embedding(text)

    embedding = model.encode(text)
    return np.asarray(embedding, dtype="float32")


def get_embedding_dim():
    model = _load_model()

    if model is None:
        return FALLBACK_DIM

    return int(model.get_sentence_embedding_dimension())
