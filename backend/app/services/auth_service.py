from sqlalchemy.orm import Session
from app.core.security import verify_password, hash_password, create_access_token
from app.core.constants import ACTIVATION_CODES
from app.models.user import User
from app.schemas.auth import TokenResponse

def authenticate(db: Session, username: str, password: str) -> TokenResponse | None:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None

    token = create_access_token(subject=user.username, extra_claims={"role": user.role, "uid": user.id})
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        username=user.username,
        role=user.role,
    )

def register_with_code(
    db: Session,
    username: str,
    full_name: str,
    password: str,
    role: str,
    activation_code: str,
    department_id: int | None,
    team_id: int | None,
    member_type: str,
):
    expected = ACTIVATION_CODES.get(role)
    if expected is None or activation_code != expected:
        return False, "⛔ كود التفعيل غير صحيح!"

    if db.query(User).filter(User.username == username).first():
        return False, "⚠️ اسم المستخدم موجود"

    user = User(
        username=username,
        full_name=full_name,
        password_hash=hash_password(password),
        role=role,
        member_type=member_type,
        team_id=team_id,
        department_id=department_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return True, "✅ تم الإنشاء"
