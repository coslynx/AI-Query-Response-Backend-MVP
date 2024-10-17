from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class QueryResponse(Base):
    __tablename__ = "query_responses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query = Column(String, nullable=False)
    model = Column(String, nullable=False)
    response = Column(Text, nullable=False)

    user = relationship("User", backref="query_responses")