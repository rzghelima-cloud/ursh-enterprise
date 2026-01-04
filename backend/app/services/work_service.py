from datetime import date
import json
import pandas as pd
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text

from app.models.work import Work
from app.models.user import User

BASE_REPORT_SQL = """
SELECT
    w.id, w.user_id, w.title, w.activity_type, w.publication_date, w.year, w.points, w.classification, w.details,
    u.full_name as researcher,
    t.name as team,
    d.name_ar as department
FROM works w
JOIN users u ON w.user_id = u.id
LEFT JOIN teams t ON u.team_id = t.id
LEFT JOIN departments d ON u.department_id = d.id
"""

def can_access_work(actor: User, work_owner: User) -> bool:
    # Admin: everything
    if actor.role == "admin":
        return True
    # Dept head: same department
    if actor.role == "dept_head" and actor.department_id and actor.department_id == work_owner.department_id:
        return True
    # Leader: same team
    if actor.role == "leader" and actor.team_id and actor.team_id == work_owner.team_id:
        return True
    # Researcher: self
    return actor.id == work_owner.id

def create_work(db: Session, actor: User, title: str, details: dict | None, activity_type: str, classification: str,
                publication_date: date, points: int):
    w = Work(
        user_id=actor.id,
        title=title,
        details=json.dumps(details or {}, ensure_ascii=False),
        activity_type=activity_type,
        classification=classification,
        publication_date=publication_date,
        year=publication_date.year,
        points=points,
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return w

def update_work(db: Session, actor: User, work_id: int, title: str | None, publication_date: date | None) -> bool:
    w = db.query(Work).options(joinedload(Work.researcher)).filter(Work.id == work_id).first()
    if not w:
        return False
    owner = w.researcher
    if not can_access_work(actor, owner):
        return False
    if title is not None:
        w.title = title
    if publication_date is not None:
        w.publication_date = publication_date
        w.year = publication_date.year
    db.add(w)
    db.commit()
    return True

def delete_work(db: Session, actor: User, work_id: int) -> bool:
    w = db.query(Work).options(joinedload(Work.researcher)).filter(Work.id == work_id).first()
    if not w:
        return False
    if not can_access_work(actor, w.researcher):
        return False
    db.delete(w)
    db.commit()
    return True

def get_smart_report_df(
    db: Session,
    actor: User,
    date_from: date | None = None,
    date_to: date | None = None,
    year: int | None = None,
    department: str | None = None,
    team: str | None = None,
    activity_type: str | None = None,
    search: str | None = None,
):
    # Use pandas read_sql against same engine via SQLAlchemy connection
    conn = db.get_bind().connect()
    try:
        df = pd.read_sql(text(BASE_REPORT_SQL), conn)
    finally:
        conn.close()

    if df.empty:
        return df

    df["department"] = df["department"].fillna("غير محدد")
    df["team"] = df["team"].fillna("غير محدد")
    df["activity_type"] = df["activity_type"].fillna("غير محدد")
    df["publication_date"] = pd.to_datetime(df["publication_date"]).dt.date

    # Role filtering
    if actor.role == "admin":
        scoped = df
    elif actor.role == "dept_head":
        if actor.department and actor.department.name_ar:
            scoped = df[df["department"] == actor.department.name_ar]
        else:
            scoped = df.iloc[0:0]
    elif actor.role == "leader":
        if actor.team and actor.team.name:
            scoped = df[df["team"] == actor.team.name]
        else:
            scoped = df.iloc[0:0]
    else:
        scoped = df[df["user_id"] == actor.id]

    # Optional filters
    if year is not None:
        scoped = scoped[scoped["year"] == year]
    else:
        if date_from is not None:
            scoped = scoped[scoped["publication_date"] >= date_from]
        if date_to is not None:
            scoped = scoped[scoped["publication_date"] <= date_to]

    if department and department != "الكل":
        scoped = scoped[scoped["department"] == department]
    if team and team != "الكل":
        scoped = scoped[scoped["team"] == team]
    if activity_type and activity_type != "الكل":
        scoped = scoped[scoped["activity_type"] == activity_type]
    if search:
        mask = scoped["title"].fillna("").str.contains(search, na=False) | scoped["researcher"].fillna("").str.contains(search, na=False)
        scoped = scoped[mask]

    return scoped

def get_user_works_df(db: Session, user_id: int):
    conn = db.get_bind().connect()
    try:
        df = pd.read_sql(text(BASE_REPORT_SQL + " WHERE w.user_id = :uid"), conn, params={"uid": user_id})
    finally:
        conn.close()
    if df.empty:
        return df
    df["publication_date"] = pd.to_datetime(df["publication_date"]).dt.date
    return df
