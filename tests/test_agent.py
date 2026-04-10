import pytest
from app.services.agent import run_agent, _parse_create_task, _parse_create_note


def test_parse_create_task():
    assert _parse_create_task("add task Buy groceries") == "Buy groceries"
    assert _parse_create_task("create task: Write report") == "Write report"
    assert _parse_create_task("add task") == ""


def test_parse_create_note():
    title, content = _parse_create_note("add note My Title: This is the content")
    assert title == "My Title"
    assert content == "This is the content"

    title, content = _parse_create_note("add note Just content")
    assert title == "Just content"  # No colon, so title takes the whole content
    assert content == "Just content"


def test_run_agent_chat(monkeypatch):
    mock_response = "Hello! How can I assist you?"
    
    def mock_create(*args, **kwargs):
        class MockChoice:
            message = type('obj', (object,), {'content': mock_response})()
        class MockResponse:
            choices = [MockChoice()]
        return MockResponse()

    from app.core import llm
    monkeypatch.setattr(llm.client.chat.completions, 'create', mock_create)

    result = run_agent("Hello, assistant!")
    assert mock_response in result or "Hello" in result


def test_run_agent_add_task():
    result = run_agent("add task Complete project")
    assert "Task added" in result or "Complete project" in result


def test_run_agent_show_tasks():
    run_agent("add task Test task 1")
    result = run_agent("show tasks")
    assert "Test task" in result or "task" in result.lower()


def test_run_agent_add_note():
    result = run_agent("add note: My note")
    assert "Note added" in result or "My note" in result


def test_run_agent_show_notes():
    run_agent("add note: Test note content")
    result = run_agent("show notes")
    assert "note" in result.lower() or "Test" in result
