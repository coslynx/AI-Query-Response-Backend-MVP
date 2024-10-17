from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..config import settings

Base = declarative_base()

class Base(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, nullable=False, default=settings.get_current_datetime())
    updated_at = Column(String, nullable=False, default=settings.get_current_datetime(), onupdate=settings.get_current_datetime())