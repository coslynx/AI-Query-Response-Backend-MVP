from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from werkzeug.security import generate_password_hash, check_password_hash  # Version: 2.2.2

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    query_responses = relationship("QueryResponse", backref="user")