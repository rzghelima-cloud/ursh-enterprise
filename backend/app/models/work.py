from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    details = Column(Text)
    activity_type = Column(String)
    classification = Column(String)
    publication_date = Column(Date)
    year = Column(Integer)
    points = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    researcher = relationship("User", back_populates="works")
