import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings

client = TestClient(app)

@pytest.fixture
def auth_headers():
    settings = get_settings()
    return {"Authorization": f"Bearer {settings.BEARER_TOKEN}"}

def test_chat_endpoint(auth_headers):
    response = client.post(
        "/api/v1/chat",
        json={"query": "What is FastAPI?", "domain": "default"},
        headers=auth_headers
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "answer" in json_response
    assert "sources" in json_response

def test_chat_endpoint_unauthorized():
    response = client.post(
        "/api/v1/chat",
        json={"query": "What is FastAPI?", "domain": "default"},
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
