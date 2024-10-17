# Specify version and import
import pytest  # Version: 8.3.3
from fastapi.testclient import TestClient  # Version: 0.115.2
from sqlalchemy.orm import Session  # Version: 2.0.36
from api.src.core.query.services.query_service import process_query as query_service  # Version: 0.115.2
from api.src.core.db.models import QueryResponse  # Version: 2.0.36
from api.src.core.db.utils.db_utils import create_query_response  # Version: 2.9.2
from api.src.core.query.schemas import QueryRequest, QueryResponse as QueryResponseSchema  # Version: 2.9.2
from api.src.config.settings import Settings  # Version: 2.9.2
from api.src.exceptions.base_exception import QueryError  # Version: 2.9.2
from api.src.tests.conftest import client, session, new_user, new_query_response  # Version: 2.9.2
from typing import Optional  # Version: 2.9.2
import openai  # Version: 1.52.0
from unittest.mock import patch  # Version: 3.11.1
from api.src.utils.openai_utils import make_openai_request  # Version: 2.9.2
from api.src.core.db.utils.db_utils import get_db  # Version: 2.9.2
from api.src.main import app

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY

def test_process_query_success(client: TestClient, session: Session, new_user: User):
    query_request = QueryRequest(query="What is the meaning of life?", model="text-davinci-003", user_id=new_user.id)
    with patch("api.src.core.query.services.query_service.make_openai_request") as mock_openai_request:
        mock_openai_request.return_value = "The meaning of life is 42."
        response = client.post("/query", json=query_request.dict())
        assert response.status_code == 200
        assert response.json()["response"] == "The meaning of life is 42."
        assert response.json()["query_id"] is not None
        query_response = session.query(QueryResponse).filter_by(id=response.json()["query_id"]).first()
        assert query_response.query == query_request.query
        assert query_response.model == query_request.model
        assert query_response.response == "The meaning of life is 42."
        assert query_response.user_id == new_user.id

def test_process_query_openai_api_error(client: TestClient, session: Session, new_user: User):
    query_request = QueryRequest(query="What is the meaning of life?", model="text-davinci-003", user_id=new_user.id)
    with patch("api.src.core.query.services.query_service.make_openai_request") as mock_openai_request:
        mock_openai_request.side_effect = openai.error.APIError("API Error")
        response = client.post("/query", json=query_request.dict())
        assert response.status_code == 400
        assert response.json()["detail"].startswith("OpenAI API error")

def test_process_query_database_error(client: TestClient, session: Session, new_user: User):
    query_request = QueryRequest(query="What is the meaning of life?", model="text-davinci-003", user_id=new_user.id)
    with patch("api.src.core.db.utils.db_utils.create_query_response") as mock_create_query_response:
        mock_create_query_response.side_effect = Exception("Database Error")
        response = client.post("/query", json=query_request.dict())
        assert response.status_code == 400
        assert response.json()["detail"].startswith("Error processing query")

def test_get_query_responses(client: TestClient, session: Session, new_query_response: QueryResponse):
    response = client.get("/query/responses")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert any(query_response["id"] == new_query_response.id for query_response in response.json())

def test_get_query_responses_by_user_id(client: TestClient, session: Session, new_query_response: QueryResponse, new_user: User):
    response = client.get(f"/query/responses?user_id={new_user.id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert any(query_response["id"] == new_query_response.id for query_response in response.json())

def test_get_query_response_by_id(client: TestClient, session: Session, new_query_response: QueryResponse):
    response = client.get(f"/query/responses/{new_query_response.id}")
    assert response.status_code == 200
    assert response.json()["id"] == new_query_response.id

def test_get_query_response_not_found(client: TestClient, session: Session):
    response = client.get("/query/responses/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Query response not found"