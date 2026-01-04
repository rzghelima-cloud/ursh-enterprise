from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_roles
from app.schemas.user import UserPublic, UserCreateManual, PasswordChange
from app.models.user import User
from app.services.user_service import create_user_manual, change_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserPublic)
def me(user: User = Depends(get_current_user)):
    return UserPublic(
        id=user.id, username=user.username, full_name=user.full_name,
        role=user.role, member_type=user.member_type,
        team_id=user.team_id, department_id=user.department_id
    )

@router.post("/manual")
def add_user_manual(
    data: UserCreateManual,
    _: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    ok, msg = create_user_manual(
        db, data.username, data.full_name, data.password, data.role,
        data.department_id, data.team_id, data.member_type
    )
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

@router.post("/change-password")
def change_my_password(
    data: PasswordChange,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    change_password(db, user, data.new_password)
    return {"message": "تم التغيير بنجاح"}
