from sqlalchemy.orm import Session
from app.models.db_models import Task, Note
from app.models.schemas import TaskCreate, NoteCreate


def get_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.created_at.asc()).all()


def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(
        title=task.title.strip(),
        description=task.description or "",
        status="pending",
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_notes(db: Session) -> list[Note]:
    return db.query(Note).order_by(Note.created_at.asc()).all()


def create_note(db: Session, note: NoteCreate) -> Note:
    db_note = Note(title=note.title.strip(), content=note.content.strip())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
