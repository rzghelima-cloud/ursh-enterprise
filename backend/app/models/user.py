from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    full_name = Column(String)
    password_hash = Column(String)
    role = Column(String)
    member_type = Column(String)

    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    team = relationship("Team", back_populates="members")
    department = relationship("Department", back_populates="users")
    works = relationship("Work", back_populates="researcher")
