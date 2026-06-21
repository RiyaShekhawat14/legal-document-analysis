from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth.dependencies import get_current_user
from rag.rag_pipeline import ask_question, get_rag_status, process_document
from services.legal_assistant_service import legal_assistant_service

router = APIRouter()


class DocumentText(BaseModel):
    text: str


class Question(BaseModel):
    question: str


@router.post("/process-document")
def process_doc(data: DocumentText, current_user=Depends(get_current_user)):
    process_document(data.text, session_id=current_user.id)
    return {"message": "Document processed for chat"}


@router.post("/ask")
def ask(data: Question, current_user=Depends(get_current_user)):
    return ask_question(data.question, session_id=current_user.id)


@router.get("/status")
def status(current_user=Depends(get_current_user)):
    return {
        "assistant": legal_assistant_service.get_status(),
        "document": get_rag_status(session_id=current_user.id),
    }
