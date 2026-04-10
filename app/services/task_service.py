from app.db.database import SessionLocal
from app.db.crud import create_task as crud_create_task, get_tasks as crud_get_tasks
from app.models.schemas import TaskCreate


def add_task(title: str, description: str | None = None):
    task_data = TaskCreate(title=title, description=description)
    with SessionLocal() as db:
        return crud_create_task(db, task_data)


def list_tasks():
    with SessionLocal() as db:
        return crud_get_tasks(db)
