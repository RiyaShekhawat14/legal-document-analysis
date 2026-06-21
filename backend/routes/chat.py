from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from auth.dependencies import get_current_user
from config.settings import get_runtime_mode, save_runtime_mode, settings
from rag.rag_pipeline import ask_question, get_rag_status
from services.legal_assistant_service import legal_assistant_service

router = APIRouter()


class ChatTurn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatTurn] = Field(default_factory=list)


class AssistantModeRequest(BaseModel):
    mode: str


@router.get("/status")
def get_chat_status(current_user=Depends(get_current_user)):
    return {
        "assistant": legal_assistant_service.get_status(),
        "document": get_rag_status(session_id=current_user.id),
        "runtime_mode": get_runtime_mode(),
    }


@router.post("/ask")
def chat_with_document(chat: ChatRequest, current_user=Depends(get_current_user)):
    if not chat.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty.",
        )

    return ask_question(
        chat.message,
        history=[turn.model_dump() for turn in chat.history],
        session_id=current_user.id,
    )


@router.post("/mode")
def set_chat_mode(payload: AssistantModeRequest):
    mode = payload.mode.strip().lower()

    if mode == "fine_tuned":
        settings.LEGAL_AI_PREFERRED_LLM = "fine_tuned"
        settings.LEGAL_AI_CPU_SAFE_MODE = False
        settings.LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU = True
        settings.OLLAMA_ENABLED = False
        runtime_mode = save_runtime_mode(
            cpu_safe_mode=False,
            enable_fine_tuned_on_cpu=True,
        )
    elif mode == "ollama":
        settings.LEGAL_AI_PREFERRED_LLM = "ollama"
        settings.LEGAL_AI_CPU_SAFE_MODE = True
        settings.LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU = False
        settings.OLLAMA_ENABLED = True
        runtime_mode = save_runtime_mode(
            cpu_safe_mode=True,
            enable_fine_tuned_on_cpu=False,
        )
    elif mode == "laptop":
        settings.LEGAL_AI_PREFERRED_LLM = "fine_tuned"
        settings.LEGAL_AI_CPU_SAFE_MODE = False
        settings.LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU = True
        settings.OLLAMA_ENABLED = False
        runtime_mode = save_runtime_mode(
            cpu_safe_mode=False,
            enable_fine_tuned_on_cpu=True,
        )
    else:
        return {
            "status": "error",
            "message": "Unsupported mode. Use `fine_tuned`, `ollama`, or `laptop`.",
        }

    legal_assistant_service.reset_model()

    return {
        "status": "success",
        "message": f"Assistant mode switched to `{mode}`.",
        "preferred_llm": settings.LEGAL_AI_PREFERRED_LLM,
        "runtime_mode": runtime_mode,
        "assistant": legal_assistant_service.get_status(),
    }
