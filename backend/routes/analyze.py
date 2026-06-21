from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database import crud
from database.db import get_db
from rag.rag_pipeline import process_document
from services.advice_service import generate_advice
from services.ai_services import summarize_text
from services.clause_service import split_into_clauses
from services.clause_templates import get_clause_template, list_available_clause_types, compare_clause_versions
from services.risk_services import analyze_document_risk
from services.translation_services import translate_text
from utils.file_reader import extract_text_from_file, save_uploaded_file
from utils.logger import logger
from utils.response_formatter import success_response

router = APIRouter()


@router.post("/analyze-risk")
async def analyze_risk(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        logger.info("File uploaded: %s", file.filename)

        save_uploaded_file(file)
        file.file.seek(0)

        text = extract_text_from_file(file)
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract text from file.",
            )

        process_document(text, filename=file.filename, session_id=current_user.id)

        clauses = split_into_clauses(text)
        result = analyze_document_risk(clauses)
        summary_en = summarize_text(text)
        summary_hi = translate_text(summary_en)
        advice = generate_advice(result["overall_risk"])

        document = crud.create_document(
            db=db,
            filename=file.filename,
            content=text,
            overall_risk=result["overall_risk"],
            owner_id=current_user.id,
        )

        for clause, analysis in zip(clauses, result["clauses"]):
            crud.create_clause(
                db=db,
                clause_text=clause["text"],
                risk_level=analysis["risk"],
                document_id=document.id,
            )

        return success_response(
            {
                "document_id": document.id,
                "filename": file.filename,
                "summary_en": summary_en,
                "summary_hi": summary_hi,
                "advice": advice,
                "analysis": result,
            }
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Document analysis failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


@router.get("/clause-templates/types")
def get_available_clause_types(current_user=Depends(get_current_user)):
    """Get list of available clause template types."""
    try:
        clause_types = list_available_clause_types()
        return success_response({"clause_types": clause_types})
    except Exception as exc:
        logger.exception("Failed to get clause types: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve clause types",
        ) from exc


@router.get("/clause-templates/{clause_type}")
def get_template(
    clause_type: str,
    version: str = "standard",
    current_user=Depends(get_current_user),
):
    """Get a specific clause template."""
    try:
        template = get_clause_template(clause_type, version)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clause template '{clause_type}' not found",
            )
        return success_response(template)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get template: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve template",
        ) from exc


@router.get("/clause-templates/{clause_type}/compare")
def compare_templates(
    clause_type: str,
    current_user=Depends(get_current_user),
):
    """Compare all versions of a clause template."""
    try:
        comparison = compare_clause_versions(clause_type)
        if not comparison:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clause type '{clause_type}' not found",
            )
        return success_response(comparison)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to compare templates: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to compare templates",
        ) from exc
