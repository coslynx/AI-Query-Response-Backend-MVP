# Specify version and import
from fastapi import APIRouter, Depends, HTTPException  # Version: 0.115.2
from typing import Optional  # Version: 2.9.2
from sqlalchemy.orm import Session  # Version: 2.0.36
from ..database import get_db  # Version: 2.0.36
from .services import auth_service  # Version: 0.115.2
from .schemas import User, Token  # Version: 2.9.2
from ..exceptions.base_exception import AuthenticationError  # Version: 2.9.2

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

# Authentication Endpoint - POST /auth/login
@auth_router.post("/login", response_model=Token)
async def login(user: User, db: Session = Depends(get_db)):
    """
    Logs in a user, validates credentials, and generates a JWT access token.

    Args:
        user (User): Pydantic model containing user's email and password.
        db (Session): SQLAlchemy database session.

    Returns:
        Token: Pydantic model containing the JWT access token.

    Raises:
        HTTPException: If authentication fails (invalid credentials).
    """
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db or not user_db.check_password(user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth_service.create_access_token(data={"sub": user_db.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Endpoint - GET /auth/me
@auth_router.get("/me", response_model=User, dependencies=[Depends(auth_service.authenticate_user)])
async def get_me(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Retrieves the currently authenticated user's information.

    Args:
        current_user (User): Pydantic model containing user's data (obtained from JWT).
        db (Session): SQLAlchemy database session.

    Returns:
        User: Pydantic model containing the authenticated user's information.
    """
    return current_user