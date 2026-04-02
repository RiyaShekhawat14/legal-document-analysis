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


def create_document(db, filename, content, overall_risk):
    doc = models.Document(
        filename=filename,
        content=content,
        overall_risk=overall_risk
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

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