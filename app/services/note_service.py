from app.db.database import SessionLocal
from app.db.crud import create_note as crud_create_note, get_notes as crud_get_notes
from app.models.schemas import NoteCreate


def add_note(title: str, content: str):
    note_data = NoteCreate(title=title, content=content)
    with SessionLocal() as db:
        return crud_create_note(db, note_data)


def list_notes():
    with SessionLocal() as db:
        return crud_get_notes(db)
