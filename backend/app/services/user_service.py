from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User

def create_user_manual(
    db: Session,
    username: str,
    full_name: str,
    password: str,
    role: str,
    department_id: int | None,
    team_id: int | None,
    member_type: str,
):
    if db.query(User).filter(User.username == username).first():
        return False, "موجود مسبقاً"
    user = User(
        username=username,
        full_name=full_name,
        password_hash=hash_password(password),
        role=role,
        department_id=department_id,
        team_id=team_id,
        member_type=member_type,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return True, "تمت الإضافة"

def change_password(db: Session, user: User, new_password: str) -> bool:
    user.password_hash = hash_password(new_password)
    db.add(user)
    db.commit()
    return True
