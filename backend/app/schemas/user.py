from pydantic import BaseModel

class UserPublic(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    member_type: str
    team_id: int | None = None
    department_id: int | None = None

class UserCreateManual(BaseModel):
    username: str
    full_name: str
    password: str
    role: str
    department_id: int | None = None
    team_id: int | None = None
    member_type: str = "permanent"

class PasswordChange(BaseModel):
    new_password: str
