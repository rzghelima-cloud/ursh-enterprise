from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.api.deps import get_db, get_current_user
from app.schemas.org import DepartmentPublic, TeamPublic
from app.schemas.user import UserPublic
from app.models.department import Department
from app.models.team import Team
from app.models.user import User

router = APIRouter(prefix="/org", tags=["Organization"])

# ✅ Public (needed for self-signup forms)
@router.get("/departments", response_model=list[DepartmentPublic])
def departments(db: Session = Depends(get_db)):
    depts = db.query(Department).order_by(Department.id).all()
    return [DepartmentPublic(id=d.id, name_ar=d.name_ar, name_la=d.name_la, short_name=d.short_name, head_name=d.head_name) for d in depts]

# ✅ Public (needed for self-signup forms)
@router.get("/teams", response_model=list[TeamPublic])
def teams(db: Session = Depends(get_db), department_id: int | None = None):
    q = db.query(Team).order_by(Team.id)
    if department_id is not None:
        q = q.filter(Team.department_id == department_id)
    teams = q.all()
    return [
        TeamPublic(
            id=t.id, name=t.name, name_en=t.name_en, short_name=t.short_name, head_name=t.head_name,
            description=t.description, classification=t.classification, domains=t.domains, keywords=t.keywords,
            program_desc=t.program_desc, department_id=t.department_id
        ) for t in teams
    ]

# 🔒 Authenticated (full org details with members)
@router.get("/departments/{dept_id}/full")
def department_full(dept_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    d = db.query(Department).options(joinedload(Department.teams).joinedload(Team.members)).filter(Department.id == dept_id).first()
    if not d:
        return {"department": None, "teams": []}

    dept = DepartmentPublic(id=d.id, name_ar=d.name_ar, name_la=d.name_la, short_name=d.short_name, head_name=d.head_name)
    teams = []
    for t in d.teams:
        members = [
            UserPublic(
                id=m.id, username=m.username, full_name=m.full_name, role=m.role, member_type=m.member_type,
                team_id=m.team_id, department_id=m.department_id
            ) for m in t.members
        ]
        teams.append({
            "team": TeamPublic(
                id=t.id, name=t.name, name_en=t.name_en, short_name=t.short_name, head_name=t.head_name,
                description=t.description, classification=t.classification, domains=t.domains, keywords=t.keywords,
                program_desc=t.program_desc, department_id=t.department_id
            ),
            "members": members,
        })
    return {"department": dept, "teams": teams}
