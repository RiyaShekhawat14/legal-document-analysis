from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from database import models

router = APIRouter()


@router.get("/")
def get_documents(db: Session = Depends(get_db)):
    documents = db.query(models.Document).all()

    result = []
    for doc in documents:
        result.append({
            "id": doc.id,
            "filename": doc.filename,
            "uploaded_at": doc.uploaded_at
        })

    return result


@router.get("/{doc_id}")
def get_document_clauses(doc_id: int, db: Session = Depends(get_db)):
    clauses = db.query(models.Clause).filter(
        models.Clause.document_id == doc_id
    ).all()

    result = []
    for clause in clauses:
        result.append({
            "text": clause.clause_text,
            "risk": clause.risk_level
        })

    return result


@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(
        models.Document.id == doc_id
    ).first()

    if doc:
        db.delete(doc)
        db.commit()
        return {"message": "Document deleted"}

    return {"message": "Document not found"}