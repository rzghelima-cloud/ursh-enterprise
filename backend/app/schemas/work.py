from datetime import date
from pydantic import BaseModel

class WorkCreate(BaseModel):
    title: str
    details: dict | None = None
    activity_type: str
    classification: str = "غير مصنف"
    publication_date: date
    points: int

class WorkUpdate(BaseModel):
    title: str | None = None
    publication_date: date | None = None

class WorkPublic(BaseModel):
    id: int
    user_id: int
    title: str
    activity_type: str
    classification: str | None = None
    publication_date: date | None = None
    year: int | None = None
    points: int | None = None
    details: str | None = None
