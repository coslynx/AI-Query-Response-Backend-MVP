from .settings import Settings

settings = Settings()

# Initialize OpenAI API (load API key from environment variable)
import openai
openai.api_key = settings.OPENAI_API_KEY

# Initialize database connection (load connection string from environment variable)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database session factory (for dependency injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Set up FastAPI app (import from main.py)
from fastapi import FastAPI
app = FastAPI()