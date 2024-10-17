# Specify version and import
import pytest  # Version: 8.3.3
from fastapi.testclient import TestClient  # Version: 0.115.2
from sqlalchemy.orm import Session  # Version: 2.0.36
from api.src.core.auth.services.auth_service import (
    authenticate_user,
    create_access_token,
)  # Version: 0.115.2
from api.src.core.db.models import User  # Version: 2.0.36
from api.src.core.auth.schemas import User as UserSchema, Token  # Version: 2.9.2
from api.src.config.settings import Settings  # Version: 2.9.2
from api.src.exceptions.base_exception import AuthenticationError  # Version: 2.9.2
from api.src.tests.conftest import client, session, new_user  # Version: 2.9.2
from unittest.mock import patch  # Version: 3.11.1
from api.src.core.auth.utils.auth_utils import hash_password  # Version: 2.9.2
from api.src.core.db.utils.db_utils import get_db  # Version: 2.9.2
from api.src.main import app

settings = Settings()

# Test for successful login
def test_login_success(client: TestClient, session: Session, new_user: User):
    user_data = {"email": new_user.email, "password": "testpassword"}
    response = client.post("/login", json=user_data)
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"

# Test for invalid credentials
def test_login_invalid_credentials(client: TestClient, session: Session, new_user: User):
    user_data = {"email": new_user.email, "password": "wrongpassword"}
    response = client.post("/login", json=user_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

# Test for creating access token
def test_create_access_token():
    user_data = {"sub": "test@example.com"}
    token = create_access_token(data=user_data)
    assert token is not None

# Test for authenticating a user
def test_authenticate_user(session: Session, new_user: User):
    user_db = authenticate_user(user=UserSchema(email=new_user.email, password="testpassword"), db=session)
    assert user_db is not None
    assert user_db.email == new_user.email

# Test for authenticating a user with invalid credentials
def test_authenticate_user_invalid_credentials(session: Session, new_user: User):
    with pytest.raises(AuthenticationError):
        authenticate_user(user=UserSchema(email=new_user.email, password="wrongpassword"), db=session)

# Test for password hashing
def test_hash_password():
    hashed_password = hash_password("testpassword")
    assert hashed_password is not None
    assert hashed_password != "testpassword"

# Test for getting the current user
def test_get_current_user(client: TestClient, session: Session, new_user: User):
    access_token = create_access_token(data={"sub": new_user.email})
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == new_user.email

# Test for handling JWT error
def test_get_current_user_jwt_error(client: TestClient, session: Session, new_user: User):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"