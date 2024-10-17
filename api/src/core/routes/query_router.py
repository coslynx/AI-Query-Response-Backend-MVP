# Specify version and import
from fastapi import APIRouter, Depends, HTTPException  # Version: 0.115.2
from typing import Optional  # Version: 2.9.2
from sqlalchemy.orm import Session  # Version: 2.0.36
from ..database import get_db  # Version: 2.0.36
from .services import query_service  # Version: 0.115.2
from .schemas import QueryRequest, QueryResponse  # Version: 2.9.2
from ..exceptions.base_exception import QueryError  # Version: 2.9.2

query_router = APIRouter(prefix="/query", tags=["query"])

#  Function Definitions
@query_router.get("/responses", response_model=list[QueryResponse])
async def get_query_responses(db: Session = Depends(get_db), user_id: Optional[int] = None):
    """Retrieves a list of query responses, optionally filtered by user ID."""
    try:
        if user_id:
            return db.query(QueryResponse).filter(QueryResponse.user_id == user_id).all()
        return db.query(QueryResponse).all()
    except Exception as e:
        raise QueryError(detail=f"Error retrieving query responses: {e}")


@query_router.get("/responses/{query_id}", response_model=QueryResponse)
async def get_query_response(query_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific query response by ID."""
    try:
        query_response = db.query(QueryResponse).filter(QueryResponse.id == query_id).first()
        if not query_response:
            raise HTTPException(status_code=404, detail="Query response not found")
        return query_response
    except Exception as e:
        raise QueryError(detail=f"Error retrieving query response: {e}")


@query_router.post("/", response_model=QueryResponse)
async def process_query(query_request: QueryRequest, db: Session = Depends(get_db)):
    """Processes a user query using OpenAI's API and stores the response."""
    try:
        response_text = await query_service.process_query(query_request, db)
        return QueryResponse(query=query_request.query, model=query_request.model, response=response_text)
    except Exception as e:
        raise QueryError(detail=f"Error processing query: {e}")