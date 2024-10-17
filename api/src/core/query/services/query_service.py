from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import openai

from ..config.settings import Settings
from ..database import get_db
from ..models import QueryResponse, User
from ..schemas import QueryRequest, QueryResponse as QueryResponseSchema
from ..utils.db_utils import create_query_response
from ..exceptions.base_exception import QueryError

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY


async def process_query(query_request: QueryRequest, db: Session):
    """Processes a user query using OpenAI's API and stores the response in the database.

    Args:
        query_request: The QueryRequest object containing the user's query and model selection.
        db: Database session.

    Returns:
        QueryResponse: The newly created QueryResponse object containing the AI-generated response.

    Raises:
        QueryError: If an error occurs during query processing or database interaction.
    """
    try:
        response = openai.Completion.create(
            engine=query_request.model,
            prompt=query_request.query,
            max_tokens=1024,
            temperature=0.5,
        )
        response_text = response.choices[0].text

        # Store the query and response in the database
        db_query = create_query_response(db, query_request, response_text)

        return db_query
    except openai.error.APIError as e:
        raise QueryError(detail=f"OpenAI API error: {e}")
    except Exception as e:
        raise QueryError(detail=f"Error processing query: {e}")