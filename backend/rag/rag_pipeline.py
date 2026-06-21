from rag.embedder import get_embedding, get_embedding_dim
from rag.vector_store import VectorStore
from services.legal_assistant_service import legal_assistant_service
from services.general_qa_service import generate_general_legal_advice

_embedding_dim = get_embedding_dim()
_user_stores: dict[str, VectorStore] = {}
_documents: dict[str, dict] = {}


def split_text(text, chunk_size=300):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks


def _normalize_session_id(session_id=None):
    return str(session_id or "global")


def _get_store(session_id=None):
    key = _normalize_session_id(session_id)
    store = _user_stores.get(key)
    if store is None:
        store = VectorStore(
            dim=_embedding_dim,
            collection_name=f"legal_document_chunks_{key}",
        )
        _user_stores[key] = store
    return store


def process_document(text, filename=None, session_id=None):
    key = _normalize_session_id(session_id)
    vector_store = _get_store(key)
    vector_store.reset()

    chunks = split_text(text)
    embeddings = [get_embedding(chunk) for chunk in chunks]
    vector_store.add_embeddings(embeddings, chunks)
    _documents[key] = {
        "filename": filename,
        "chunk_count": len(chunks),
    }


def retrieve_context(question, k=3, session_id=None):
    vector_store = _get_store(session_id)
    query_embedding = get_embedding(question)
    return vector_store.search(query_embedding, k=k)


def get_rag_status(session_id=None):
    key = _normalize_session_id(session_id)
    current_document = _documents.get(
        key,
        {"filename": None, "chunk_count": 0},
    )
    vector_store = _get_store(key)
    return {
        "document_loaded": bool(current_document["chunk_count"]),
        "filename": current_document["filename"],
        "chunk_count": current_document["chunk_count"],
        "vector_store": vector_store.get_status(),
    }


def ask_question(question, history=None, k=3, session_id=None):
    """
    Answer a legal question using document context if available,
    or general legal knowledge if no document is loaded.
    """
    doc_status = get_rag_status(session_id=session_id)
    has_document = doc_status["document_loaded"]

    if not has_document:
        result = generate_general_legal_advice(question)
        result["sources"] = []
        result["document"] = doc_status
        result["assistant"] = legal_assistant_service.get_status()
        return result

    context_chunks = retrieve_context(question, k=k, session_id=session_id)
    result = legal_assistant_service.answer_question(
        question,
        context_chunks,
        history=history,
    )
    result["sources"] = context_chunks
    result["document"] = doc_status
    result["assistant"] = legal_assistant_service.get_status()
    return result
