from fastapi import APIRouter, Depends, File, UploadFile

from auth.dependencies import get_current_user
from services.ai_services import summarize_text
from services.clause_service import split_into_clauses
from services.risk_services import analyze_document_risk
from utils.file_reader import extract_text_from_file

router = APIRouter()


@router.post("/")
async def compare_documents(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    text1 = extract_text_from_file(file1)
    file1.file.seek(0)
    text2 = extract_text_from_file(file2)

    clauses1 = split_into_clauses(text1)
    clauses2 = split_into_clauses(text2)

    result1 = analyze_document_risk(clauses1)
    result2 = analyze_document_risk(clauses2)

    summary1 = summarize_text(text1)
    summary2 = summarize_text(text2)

    return {
        "document1": {
            "summary": summary1,
            "risk": result1["overall_risk"],
            "clauses": result1["clauses"],
        },
        "document2": {
            "summary": summary2,
            "risk": result2["overall_risk"],
            "clauses": result2["clauses"],
        },
    }
