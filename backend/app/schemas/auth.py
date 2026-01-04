from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=2)
    password: str = Field(..., min_length=3)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    role: str

class RegisterRequest(BaseModel):
    full_name: str
    username: str
    password: str
    role: str
    activation_code: str
    department_id: int | None = None
    team_id: int | None = None
    member_type: str = "permanent"
