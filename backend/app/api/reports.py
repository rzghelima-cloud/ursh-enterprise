from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.report import WorkReportRow
from app.services.work_service import get_smart_report_df

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/works", response_model=list[WorkReportRow])
def works_report(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    year: int | None = Query(default=None),
    department: str | None = Query(default=None),
    team: str | None = Query(default=None),
    activity_type: str | None = Query(default=None),
    search: str | None = Query(default=None),
):
    # Ensure relationships for role scoping (dept/team names)
    user = db.query(User).options(joinedload(User.team), joinedload(User.department)).filter(User.id == user.id).first()
    df = get_smart_report_df(db, user, date_from, date_to, year, department, team, activity_type, search)
    rows = []
    if df is None or df.empty:
        return rows
    for _, r in df.iterrows():
        rows.append(WorkReportRow(
            id=int(r["id"]),
            user_id=int(r["user_id"]),
            title=r.get("title"),
            activity_type=r.get("activity_type"),
            publication_date=r.get("publication_date"),
            year=int(r["year"]) if r.get("year") is not None else None,
            points=int(r["points"]) if r.get("points") is not None else None,
            classification=r.get("classification"),
            details=r.get("details"),
            researcher=r.get("researcher"),
            team=r.get("team"),
            department=r.get("department"),
        ))
    return rows
