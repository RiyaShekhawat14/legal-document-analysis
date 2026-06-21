import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from rag.rag_pipeline import ask_question, get_rag_status, process_document
from services.legal_assistant_service import legal_assistant_service


SAMPLE_DOCUMENT = """
MASTER SERVICES AGREEMENT

Termination. Either party may terminate this Agreement with 30 days written notice.
The customer must pay all undisputed invoices within 15 days of receipt.
If payment is late, a penalty of 2 percent per month may apply.
The supplier's liability is capped at the fees paid in the previous 12 months.
Confidential information must not be disclosed to third parties without prior written consent.
""".strip()


def main():
    print("Assistant status before loading:")
    print(legal_assistant_service.get_status())
    print()

    process_document(SAMPLE_DOCUMENT, filename="sample_msa.txt", session_id="debug")
    print("RAG status after indexing sample document:")
    print(get_rag_status(session_id="debug"))
    print()

    result = ask_question(
        "What does the contract say about termination and payment penalties?",
        session_id="debug",
    )

    print("Assistant answer:")
    print(result["answer"])
    print()
    print("Answer mode:", result["mode"])
    print("Used context chunks:", result.get("used_context_chunks"))
    print("Retrieved source chunks:")
    for index, chunk in enumerate(result.get("sources", []), start=1):
        print(f"[{index}] {chunk}")


if __name__ == "__main__":
    main()
