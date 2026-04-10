from app.services.note_service import add_note as service_add_note, list_notes as service_list_notes


def add_note(title: str, content: str):
    return service_add_note(title, content)


def get_notes():
    return service_list_notes()
