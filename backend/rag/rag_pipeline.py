from rag.embedder import get_embedding
from rag.vector_store import VectorStore

vector_store = VectorStore()


def split_text(text, chunk_size=300):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks


def process_document(text):
    global vector_store
    vector_store = VectorStore()  # Reset for new document

    chunks = split_text(text)
    embeddings = [get_embedding(chunk) for chunk in chunks]
    vector_store.add_embeddings(embeddings, chunks)


def generate_answer(question, context_chunks):
    if not context_chunks:
        return "No relevant information found in the document."

    answer = f"Question: {question}\n\n"
    answer += "Based on the document, here is the relevant information:\n\n"

    for chunk in context_chunks:
        answer += chunk + "\n\n"

    return answer


def ask_question(question):
    query_embedding = get_embedding(question)
    results = vector_store.search(query_embedding)

    answer = generate_answer(question, results)
    return answer