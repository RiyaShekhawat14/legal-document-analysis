from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from utils.file_reader import extract_text_from_file, save_uploaded_file
from services.clause_service import split_into_clauses
from services.risk_services import analyze_document_risk
from services.ai_services import summarize_text
from services.translation_services import translate_text
from services.advice_service import generate_advice

from utils.response_formatter import success_response, error_response
from utils.logger import logger

from database.db import get_db
from database import crud

from rag.rag_pipeline import process_document
router = APIRouter()


@router.post("/analyze-risk")
async def analyze_risk(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        logger.info(f"File uploaded: {file.filename}")

        # Save file
        file_path = save_uploaded_file(file)

        # Reset file pointer
        file.file.seek(0)

        # Extract text
        text = extract_text_from_file(file)
        
        if not text:
            return error_response("Could not extract text from file")   
        #Send document to Rag system
        process_document(text)

        if not text:
            return error_response("Could not extract text from file")

        # Split clauses
        clauses = split_into_clauses(text)

        # Risk analysis
        result = analyze_document_risk(clauses)

        # Generate summary (English)
        summary_en = summarize_text(text)

        # Generate Hindi summary
        summary_hi = translate_text(summary_en)

        # Generate advice
        advice = generate_advice(result["overall_risk"])

        # Save document in DB
        document = crud.create_document(
            db=db,
            filename=file.filename,
            content=text,
            overall_risk=result["overall_risk"]
        )

        # Save clauses in DB
        for clause, analysis in zip(clauses, result["clauses"]):
            crud.create_clause(
                db=db,
                clause_text=clause["text"],
                risk_level=analysis["risk"],
                document_id=document.id
            )

        return success_response({
            "document_id": document.id,
            "filename": file.filename,
            "summary_en": summary_en,
            "summary_hi": summary_hi,
            "advice": advice,
            "analysis": result
        })

    except Exception as e:
        logger.error(str(e))
        return error_response(str(e))