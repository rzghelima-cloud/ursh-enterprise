from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_roles
from app.schemas.work import WorkCreate, WorkUpdate, WorkPublic
from app.models.user import User
from app.services.work_service import create_work, update_work, delete_work

router = APIRouter(prefix="/works", tags=["Works"])

@router.post("", response_model=WorkPublic)
def create(data: WorkCreate, user: User = Depends(require_roles("leader", "researcher")), db: Session = Depends(get_db)):
    w = create_work(
        db=db,
        actor=user,
        title=data.title,
        details=data.details,
        activity_type=data.activity_type,
        classification=data.classification,
        publication_date=data.publication_date,
        points=data.points,
    )
    return WorkPublic(
        id=w.id, user_id=w.user_id, title=w.title, activity_type=w.activity_type,
        classification=w.classification, publication_date=w.publication_date,
        year=w.year, points=w.points, details=w.details
    )

@router.put("/{work_id}")
def update(work_id: int, data: WorkUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ok = update_work(db, user, work_id, data.title, data.publication_date)
    if not ok:
        raise HTTPException(status_code=403, detail="Forbidden or not found")
    return {"message": "تم التعديل"}

@router.delete("/{work_id}")
def delete(work_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ok = delete_work(db, user, work_id)
    if not ok:
        raise HTTPException(status_code=403, detail="Forbidden or not found")
    return {"message": "تم الحذف"}
