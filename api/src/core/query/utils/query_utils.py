#  Import Statements:

#  Core modules:
from typing import Optional

#  Third-party:
from fastapi import HTTPException # Version 0.115.2 

#  Internal:
from ..schemas import QueryResponse # Version 2.9.2
from ..models import QueryResponse # Version 2.9.2
from ..exceptions.base_exception import QueryError # Version 2.9.2
from ..utils.common_utils import format_datetime
from ...config.settings import Settings # Version 2.9.2

settings = Settings()


#  File Structure and Components:

#  Main Function:
def format_response(response: str, query_response: QueryResponse, user_id: Optional[int] = None) -> dict:
    """
    Formats the AI response for presentation to the user.

    Args:
        response (str): The AI-generated response text.
        query_response (QueryResponse): The QueryResponse object from the database.
        user_id (Optional[int], optional): The user ID associated with the query. Defaults to None.

    Returns:
        dict: A dictionary containing the formatted response.
    """
    formatted_response = {
        "id": query_response.id,
        "query": query_response.query,
        "model": query_response.model,
        "response": response,
        "created_at": format_datetime(query_response.created_at),
        "updated_at": format_datetime(query_response.updated_at),
        "user_id": user_id,
    }
    return formatted_response