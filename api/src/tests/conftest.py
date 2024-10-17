import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from api.src.core.db.models import Base
from api.src.core.db.models import QueryResponse, User
from api.src.config.settings import Settings
from api.src.database import engine as database_engine

# Specify version and import
from typing import Generator  # Version: 2.9.2
from fastapi.testclient import TestClient  # Version: 0.115.2
from fastapi import FastAPI  # Version: 0.115.2

settings = Settings()
database_url = settings.DATABASE_URL

# Specify version and import
import openai  # Version: 1.52.0
import os  #  No specific version required

openai.api_key = settings.OPENAI_API_KEY

@pytest.fixture(scope="session", autouse=True)
def create_tables():
  """Creates database tables for testing."""
  Base.metadata.create_all(bind=database_engine)

@pytest.fixture(scope="session")
def engine():
  """Returns the SQLAlchemy engine."""
  return create_engine(database_url)

@pytest.fixture(scope="session")
def session(engine: create_engine) -> Generator:
  """Creates a SQLAlchemy session for testing."""
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@pytest.fixture(scope="session")
def app() -> FastAPI:
  """Creates the FastAPI app for testing."""
  from api.src.main import app
  return app

@pytest.fixture(scope="function")
def client(app: FastAPI) -> TestClient:
  """Creates a test client for the FastAPI app."""
  return TestClient(app)

@pytest.fixture(scope="function")
def new_user(session: sessionmaker):
  """Creates a new user for testing."""
  user = User(email="test@example.com", hashed_password="testpassword")
  session.add(user)
  session.commit()
  session.refresh(user)
  yield user
  session.delete(user)
  session.commit()

@pytest.fixture(scope="function")
def new_query_response(session: sessionmaker):
  """Creates a new query response for testing."""
  query_response = QueryResponse(
    user_id=1,
    query="What is the meaning of life?",
    model="text-davinci-003",
    response="The meaning of life is 42.",
  )
  session.add(query_response)
  session.commit()
  session.refresh(query_response)
  yield query_response
  session.delete(query_response)
  session.commit()

@pytest.fixture(scope="function", autouse=True)
def set_up_db(session: sessionmaker):
  """Sets up the database for testing."""
  session.begin_nested()
  yield
  session.rollback()