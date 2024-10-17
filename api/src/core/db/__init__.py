from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..config.settings import Settings
from ..database import get_db
from .models import QueryResponse, User
from .schemas import QueryResponse as QueryResponseSchema, User as UserSchema
from .utils.db_utils import get_db

db_router = APIRouter(prefix="/db", tags=["database"])

@db_router.get("/query_responses", response_model=list[QueryResponseSchema])
async def get_query_responses(db: Session = Depends(get_db), user_id: Optional[int] = None):
    """Retrieves a list of query responses.

    Args:
        db: Database session.
        user_id: Optional user ID to filter responses by.

    Returns:
        A list of QueryResponseSchema objects.
    """
    if user_id:
        return db.query(QueryResponse).filter(QueryResponse.user_id == user_id).all()
    return db.query(QueryResponse).all()

@db_router.get("/query_responses/{query_id}", response_model=QueryResponseSchema)
async def get_query_response(query_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific query response by ID.

    Args:
        query_id: ID of the query response.
        db: Database session.

    Returns:
        A QueryResponseSchema object.
    """
    query_response = db.query(QueryResponse).filter(QueryResponse.id == query_id).first()
    if not query_response:
        raise HTTPException(status_code=404, detail="Query response not found")
    return query_response

@db_router.get("/users", response_model=list[UserSchema])
async def get_users(db: Session = Depends(get_db)):
    """Retrieves a list of users.

    Args:
        db: Database session.

    Returns:
        A list of UserSchema objects.
    """
    return db.query(User).all()

@db_router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific user by ID.

    Args:
        user_id: ID of the user.
        db: Database session.

    Returns:
        A UserSchema object.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user