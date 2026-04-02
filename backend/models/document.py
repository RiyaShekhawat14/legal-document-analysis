from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ClauseResponse(BaseModel):
    clause_type: str
    risk: str
    confidence: Optional[float]


class DocumentUploadResponse(BaseModel):
    filename: str
    overall_risk: str
    clauses: List[ClauseResponse]


class DocumentBase(BaseModel):
    filename: str
    content: str


class DocumentCreate(DocumentBase):
    owner_id: int


class DocumentResponse(DocumentBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True