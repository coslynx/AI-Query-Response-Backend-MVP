from typing import Optional, Dict, Any
import json

from fastapi import HTTPException  # Version 0.115.2
from openai import Completion, APIError  # Version 1.52.0

from ..exceptions.base_exception import QueryError  # Version 2.9.2
from ...config.settings import Settings  # Version 2.9.2

settings = Settings()

async def make_openai_request(query: str, model: str, max_tokens: int = 1024, temperature: float = 0.5) -> str:
    """
    Sends a request to the OpenAI API to generate text completion.

    Args:
        query (str): The user's query text.
        model (str): The OpenAI model to use for processing the query.
        max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 1024.
        temperature (float, optional): The temperature parameter controls the randomness of the generated text. Defaults to 0.5.

    Returns:
        str: The AI-generated response text.

    Raises:
        QueryError: If an error occurs during OpenAI API interaction.
    """

    try:
        response = await Completion.create(
            engine=model,
            prompt=query,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        response_text = response.choices[0].text
        return response_text
    except APIError as e:
        raise QueryError(detail=f"OpenAI API error: {e}")
    except Exception as e:
        raise QueryError(detail=f"Error processing query: {e}")