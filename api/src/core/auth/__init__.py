# Specify version and import
from fastapi import APIRouter  # Version: 0.115.2
from typing import Optional  # Version: 2.9.2
from fastapi.security import OAuth2PasswordBearer  # Version: 0.115.2
from jose import JWTError, jwt  # Version: 2.9.0
from .services.auth_service import authenticate_user, create_access_token  # Version: 0.115.2
from .models.auth_model import User  # Version: 0.115.2
from .schemas import Token  # Version: 2.9.2
from ..config.settings import Settings  # Version: 2.9.2
from ..exceptions.base_exception import AuthenticationError  # Version: 2.9.2

# Specify version and import
import os  #  No specific version required

JWT_SECRET_KEY = Settings().JWT_SECRET_KEY  # Import from settings.py

# Specify version and import
from fastapi.responses import JSONResponse  # Version: 0.115.2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

auth_router = APIRouter()

@auth_router.post("/login", tags=["authentication"])
async def login(user: User, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db or not user_db.check_password(user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user_db.email})
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})

@auth_router.get("/me", tags=["authentication"], dependencies=[Depends(authenticate_user)])
async def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user