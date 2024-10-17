# Specify version and import
from fastapi import HTTPException  # Version: 0.115.2
from typing import Optional  # Version: 2.9.2

# Specify version and import
from pydantic import BaseModel  # Version: 2.9.2

class BaseException(Exception):
    \"\"\"Base class for all custom exceptions in the application.\"\"\"\n\n    def __init__(self, status_code: int = 400, detail: str = \"An unexpected error occurred.\"):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class AuthenticationError(BaseException):
    \"\"\"Exception raised when authentication fails.\"\"\"\
    status_code = 401


class AuthorizationError(BaseException):
    \"\"\"Exception raised when authorization fails.\"\"\"\
    status_code = 403


class DatabaseError(BaseException):
    \"\"\"Exception raised when a database operation fails.\"\"\"\


class QueryError(BaseException):
    \"\"\"Exception raised when a query processing operation fails.\"\"\"\