from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import authenticate, register_with_code

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    token = authenticate(db, data.username, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    ok, msg = register_with_code(
        db=db,
        username=data.username,
        full_name=data.full_name,
        password=data.password,
        role=data.role,
        activation_code=data.activation_code,
        department_id=data.department_id,
        team_id=data.team_id,
        member_type=data.member_type,
    )
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}
