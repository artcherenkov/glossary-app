# app/models.py

from sqlalchemy import Column, Integer, String
from .database import Base


class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
