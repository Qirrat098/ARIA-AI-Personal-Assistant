import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import init_db
from unittest.mock import MagicMock, patch

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup():
    init_db()
    yield


def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


@patch('app.services.agent.client.chat.completions.create')
def test_chat_endpoint(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello! How can I help?"
    mock_create.return_value = mock_response
    
    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 200
    assert "response" in response.json()


def test_create_task():
    response = client.post("/tasks", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_get_tasks():
    client.post("/tasks", json={"title": "Task 1"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create_note():
    response = client.post("/notes", json={"title": "Test Note", "content": "Note content"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Note"


def test_get_notes():
    client.post("/notes", json={"title": "Note 1", "content": "Content 1"})
    response = client.get("/notes")
    assert response.status_code == 200
    assert len(response.json()) > 0
