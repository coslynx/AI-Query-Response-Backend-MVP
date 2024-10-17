from pydantic import BaseModel, validator
from typing import Optional

# Import the openai package (version 1.52.0) to interact with the OpenAI API.
# This is used for processing queries and generating AI responses.
import openai

# Import the configuration settings from src/config/settings.py.
# This provides access to environment variables and application settings.
from src.config.settings import Settings

# Import the base exception class from src/exceptions/base_exception.py.
# This provides a foundation for custom exception handling.
from src.exceptions.base_exception import QueryError


class QueryRequest(BaseModel):
    """
    Defines the schema for user query requests.

    Attributes:
        query (str): The user's query text.
        model (str): The OpenAI model to use for processing the query.
            Defaults to "text-davinci-003".
        user_id (Optional[int]): The user's ID, if the query is associated with a user.
    """
    query: str = Field(...)
    model: str = Field(..., regex=r"text-davinci-003|text-curie-001")
    user_id: Optional[int] = None

    @validator("query")
    def validate_query_length(cls, value):
        """
        Ensures that the query text is not longer than 500 characters.

        Args:
            value (str): The query text.

        Returns:
            str: The query text, if valid.

        Raises:
            ValueError: If the query text exceeds the maximum length.
        """
        if len(value) > 500:
            raise ValueError("Query is too long.")
        return value


class QueryResponse(BaseModel):
    """
    Defines the schema for AI-generated responses to user queries.

    Attributes:
        id (int): The unique ID of the query response.
        query (str): The user's query text.
        model (str): The OpenAI model used to process the query.
        response (str): The AI-generated response text.
        user_id (Optional[int]): The user's ID, if the query is associated with a user.
    """
    id: int
    query: str
    model: str
    response: str
    user_id: Optional[int] = None