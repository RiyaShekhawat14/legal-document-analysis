from fastapi import APIRouter
from pydantic import BaseModel

from rag.rag_pipeline import process_document, ask_question

router = APIRouter()


class DocumentText(BaseModel):
    text: str


class Question(BaseModel):
    question: str


@router.post("/process-document")
def process_doc(data: DocumentText):
    process_document(data.text)
    return {"message": "Document processed for chat"}


@router.post("/ask")
def ask(data: Question):
    answer = ask_question(data.question)
    return {"answer": answer}