from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database import crud, models
from database.db import get_db

router = APIRouter()


@router.get("/")
def get_documents(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    documents = crud.list_documents_by_owner(db, current_user.id)
    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "uploaded_at": doc.uploaded_at,
            "overall_risk": doc.overall_risk,
        }
        for doc in documents
    ]


@router.get("/{doc_id}")
def get_document_clauses(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    document = crud.get_document_by_id_and_owner(db, doc_id, current_user.id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    clauses = db.query(models.Clause).filter(models.Clause.document_id == doc_id).all()
    return [{"text": clause.clause_text, "risk": clause.risk_level} for clause in clauses]


@router.delete("/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    doc = crud.get_document_by_id_and_owner(db, doc_id, current_user.id)

    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    db.delete(doc)
    db.commit()
    return {"message": "Document deleted"}
