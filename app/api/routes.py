from fastapi import APIRouter, HTTPException
from app.services.agent import run_agent
from app.models.schemas import ChatRequest, ChatResponse, TaskCreate, TaskRead, NoteCreate, NoteRead
from app.services.task_service import add_task, list_tasks
from app.services.note_service import add_note, list_notes

router = APIRouter()


@router.get("/status")
def status():
    return {"status": "running", "message": "AI Assistant is ready"}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = run_agent(request.message)
    return ChatResponse(response=response)


@router.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate):
    return add_task(task.title, task.description)


@router.get("/tasks")
def get_tasks():
    return list_tasks()


@router.post("/notes", response_model=NoteRead)
def create_note(note: NoteCreate):
    return add_note(note.title, note.content)


@router.get("/notes")
def get_notes():
    return list_notes()
