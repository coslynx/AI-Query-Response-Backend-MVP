from pydantic import BaseModel, validator
from typing import Optional
import re

class User(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    @validator("email")
    def validate_email(cls, value):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise ValueError("Invalid email format")
        return value

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"