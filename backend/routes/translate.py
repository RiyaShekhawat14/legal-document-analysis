from fastapi import APIRouter
from pydantic import BaseModel
from services.translation_services import translate_text

router = APIRouter()


class TranslateRequest(BaseModel):
    text: str
    target_language: str = "hi"


@router.post("/")
def translate_document(request: TranslateRequest):
    translated = translate_text(request.text, target_language=request.target_language)
    return {
        "original": request.text,
        "translated": translated,
        "target_language": request.target_language,
    }