from sqlalchemy.orm import Session
from database import models


def create_user(db: Session, username: str, password: str):
    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_document(
    db: Session,
    filename: str,
    content: str,
    overall_risk: str,
    owner_id: int,
):
    doc = models.Document(
        filename=filename,
        content=content,
        overall_risk=overall_risk,
        owner_id=owner_id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def list_documents_by_owner(db: Session, owner_id: int):
    return (
        db.query(models.Document)
        .filter(models.Document.owner_id == owner_id)
        .order_by(models.Document.uploaded_at.desc())
        .all()
    )


def get_document_by_id_and_owner(db: Session, doc_id: int, owner_id: int):
    return (
        db.query(models.Document)
        .filter(models.Document.id == doc_id, models.Document.owner_id == owner_id)
        .first()
    )


def create_clause(db: Session, clause_text: str, risk_level: str, document_id: int):
    clause = models.Clause(
        clause_text=clause_text,
        risk_level=risk_level,
        document_id=document_id
    )
    db.add(clause)
    db.commit()
    db.refresh(clause)
    return clause
