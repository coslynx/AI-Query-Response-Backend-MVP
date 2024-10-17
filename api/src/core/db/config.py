from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Import the configuration settings from src/config/settings.py
from ..config.settings import Settings

settings = Settings()

# Define the database connection string using the DATABASE_URL environment variable
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the SQLAlchemy engine for connecting to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for SQLAlchemy models
Base = declarative_base()

# Create a dependency function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()