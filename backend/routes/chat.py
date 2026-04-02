from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat_with_document(chat: ChatRequest):
    return {
        "reply": "Chat feature will be implemented with AI later.",
        "your_message": chat.message
    }