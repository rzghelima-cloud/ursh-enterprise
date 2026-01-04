from pydantic import BaseModel

class DepartmentPublic(BaseModel):
    id: int
    name_ar: str | None = None
    name_la: str | None = None
    short_name: str | None = None
    head_name: str | None = None

class TeamPublic(BaseModel):
    id: int
    name: str | None = None
    name_en: str | None = None
    short_name: str | None = None
    head_name: str | None = None
    description: str | None = None
    classification: str | None = None
    domains: str | None = None
    keywords: str | None = None
    program_desc: str | None = None
    department_id: int | None = None
