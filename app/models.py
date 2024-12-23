from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "try_railway"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
