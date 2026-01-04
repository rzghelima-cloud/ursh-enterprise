from datetime import date
from pydantic import BaseModel

class WorkReportRow(BaseModel):
    id: int
    user_id: int
    title: str | None = None
    activity_type: str | None = None
    publication_date: date | None = None
    year: int | None = None
    points: int | None = None
    classification: str | None = None
    details: str | None = None
    researcher: str | None = None
    team: str | None = None
    department: str | None = None
