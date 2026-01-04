from datetime import date
from fastapi import APIRouter, Depends, Query, Response, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.services.work_service import get_smart_report_df, get_user_works_df, can_access_work
from app.services.export_service import works_to_excel
from app.services.pdf_service import generate_cv_pdf

router = APIRouter(prefix="/exports", tags=["Exports"])

@router.get("/works/excel")
def export_works_excel(
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
    user = db.query(User).options(joinedload(User.team), joinedload(User.department)).filter(User.id == user.id).first()
    df = get_smart_report_df(db, user, date_from, date_to, year, department, team, activity_type, search)
    xlsx = works_to_excel(df)
    filename = f"report_{date.today().isoformat()}.xlsx"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(content=xlsx, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

@router.get("/users/{user_id}/cv.pdf")
def export_user_cv(
    user_id: int,
    db: Session = Depends(get_db),
    actor: User = Depends(get_current_user),
):
    actor = db.query(User).options(joinedload(User.team), joinedload(User.department)).filter(User.id == actor.id).first()
    target = db.query(User).options(joinedload(User.team), joinedload(User.department)).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    # Authorization: re-use can_access_work logic using user scopes
    if not (actor.role == "admin" or
            (actor.role == "dept_head" and actor.department_id and actor.department_id == target.department_id) or
            (actor.role == "leader" and actor.team_id and actor.team_id == target.team_id) or
            (actor.id == target.id)):
        raise HTTPException(status_code=403, detail="Forbidden")

    df = get_user_works_df(db, target.id)
    org_label = target.team.name if target.team else (target.department.name_ar if target.department else "غير محدد")
    pdf_bytes = generate_cv_pdf(target.full_name, target.member_type, target.role, org_label, df)

    headers = {"Content-Disposition": f'attachment; filename="CV_{target.username}.pdf"'}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
