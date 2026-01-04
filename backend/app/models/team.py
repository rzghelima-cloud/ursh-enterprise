from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    name_en = Column(String)
    short_name = Column(String)
    head_name = Column(String)
    description = Column(Text)
    classification = Column(String)
    domains = Column(String)
    keywords = Column(String)
    program_desc = Column(Text)

    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="teams")

    members = relationship("User", back_populates="team")
