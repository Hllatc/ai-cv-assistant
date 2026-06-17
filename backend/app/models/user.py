from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

