from pydantic import BaseModel


class ClauseBase(BaseModel):
    clause_text: str
    risk_level: str
    document_id: int


class ClauseCreate(ClauseBase):
    pass


class ClauseResponse(ClauseBase):
    id: int

    class Config:
        orm_mode = True