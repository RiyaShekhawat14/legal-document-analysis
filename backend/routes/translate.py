from fastapi import APIRouter
from pydantic import BaseModel
from services.translation_services import translate_text

router = APIRouter()


class TranslateRequest(BaseModel):
    text: str
    target_language: str


@router.post("/")
def translate_text(request: TranslateRequest):
    translated = translate_text(request.text)
    return {
        "original": request.text,
        "translated": translated
    }