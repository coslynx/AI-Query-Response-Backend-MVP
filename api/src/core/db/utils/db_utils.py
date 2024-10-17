from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..config import settings
from ..database import SessionLocal, get_db

# Specify version and import
from typing import Optional # Version: 2.9.2
from fastapi.responses import JSONResponse # Version: 0.115.2
from ..exceptions.base_exception import DatabaseError # Version: 2.9.2
from ..models import QueryResponse, User # Version: 2.9.2
from ..schemas import QueryResponse as QueryResponseSchema, User as UserSchema # Version: 2.9.2


# Database Utility Functions

def get_db():
    """
    Dependency function to get a database session.

    Yields:
        Session: A database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_query_response(db: Session, query_request: QueryRequest, response: str):
    """
    Creates a new QueryResponse object in the database.

    Args:
        db: Database session.
        query_request: The QueryRequest object containing the user's query.
        response: The AI-generated response.

    Returns:
        QueryResponse: The newly created QueryResponse object.

    Raises:
        DatabaseError: If an error occurs during database interaction.
    """
    try:
        db_query = QueryResponse(query=query_request.query, model=query_request.model, response=response, user_id=query_request.user_id)
        db.add(db_query)
        db.commit()
        db.refresh(db_query)
        return db_query
    except Exception as e:
        db.rollback()
        raise DatabaseError(detail=f"Error creating query response: {e}")


def get_query_response(db: Session, query_id: int):
    """
    Retrieves a specific query response from the database by ID.

    Args:
        db: Database session.
        query_id: The ID of the query response.

    Returns:
        QueryResponse: The QueryResponse object if found, otherwise None.
    """
    try:
        return db.query(QueryResponse).filter(QueryResponse.id == query_id).first()
    except Exception as e:
        raise DatabaseError(detail=f"Error retrieving query response: {e}")


def get_query_responses(db: Session, user_id: Optional[int] = None):
    """
    Retrieves a list of query responses from the database.

    Args:
        db: Database session.
        user_id: Optional user ID to filter responses by.

    Returns:
        list[QueryResponse]: A list of QueryResponse objects, or an empty list if none are found.
    """
    try:
        if user_id:
            return db.query(QueryResponse).filter(QueryResponse.user_id == user_id).all()
        return db.query(QueryResponse).all()
    except Exception as e:
        raise DatabaseError(detail=f"Error retrieving query responses: {e}")


def get_user(db: Session, user_id: int):
    """
    Retrieves a specific user from the database by ID.

    Args:
        db: Database session.
        user_id: The ID of the user.

    Returns:
        User: The User object if found, otherwise None.
    """
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        raise DatabaseError(detail=f"Error retrieving user: {e}")


def get_users(db: Session):
    """
    Retrieves a list of all users from the database.

    Args:
        db: Database session.

    Returns:
        list[User]: A list of User objects, or an empty list if none are found.
    """
    try:
        return db.query(User).all()
    except Exception as e:
        raise DatabaseError(detail=f"Error retrieving users: {e}")