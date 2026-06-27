
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    file_path = Column(String)
    raw_text = Column(Text)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="cvs")