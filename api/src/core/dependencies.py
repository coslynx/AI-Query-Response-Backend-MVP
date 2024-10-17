from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db

# Specify version and import
from fastapi.security import OAuth2PasswordBearer # Version: 0.115.2
from jose import JWTError, jwt # Version: 2.9.0

# Specify version and import
import os  #  No specific version required 

# Specify version and import
from .auth.services.auth_service import authenticate_user  # Version: 0.115.2

# Specify version and import
from .auth.models.auth_model import User  # Version: 0.115.2

# Specify version and import
from .schemas import User # Version: 2.9.2

# Specify version and import
from .config.settings import Settings # Version: 2.9.2

# Specify version and import
from .core.auth.services.auth_service import get_current_user # Version: 0.115.2

# Specify version and import
from .core.auth.models.auth_model import User # Version: 0.115.2

JWT_SECRET_KEY = Settings().JWT_SECRET_KEY # Import from settings.py

# Specify version and import
from .core.auth.utils.auth_utils import hash_password # Version: 2.9.2

# Specify version and import
from typing import Optional # Version: 2.9.2

# Specify version and import
from fastapi.responses import JSONResponse # Version: 0.115.2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Specify version and import
from .schemas import Token # Version: 2.9.2

# Specify version and import
from .exceptions.base_exception import AuthenticationError # Version: 2.9.2

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if not username:
            raise AuthenticationError(detail="Could not validate credentials", status_code=401)
        user = db.query(User).filter(User.email == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise AuthenticationError(detail="Could not validate credentials", status_code=401)

def get_db():
    db = get_db()
    try:
        yield db
    finally:
        db.close()