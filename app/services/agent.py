import re
from app.core.llm import client
from app.core.prompts import SYSTEM_PROMPT
from app.core.config import settings
from app.services.memory import add_memory, get_memory
from app.tools.task_tools import add_task as add_task_tool, get_tasks as get_tasks_tool
from app.tools.note_tools import add_note as add_note_tool, get_notes as get_notes_tool
from app.utils.helpers import split_once, render_list


def _parse_create_task(text: str) -> str:
    cleaned = re.sub(r"^(add|create)\s+task[:\s]*", "", text, flags=re.IGNORECASE).strip()
    if not cleaned:
        return ""
    return cleaned


def _parse_create_note(text: str) -> tuple[str, str]:
    cleaned = re.sub(r"^(add|create)\s+note[:\s]*", "", text, flags=re.IGNORECASE).strip()
    title, content = split_once(cleaned, ":")
    if not content:
        title = title or "Quick note"
        content = cleaned
    return title or "Quick note", content


def run_agent(user_input: str) -> str:
    text = user_input.strip()
    text_lower = text.lower()

    if "add task" in text_lower or "create task" in text_lower:
        task_text = _parse_create_task(text)
        if not task_text:
            return "Please provide the task description."
        task = add_task_tool(task_text)
        return f"Task added: {task.title}"

    if any(trigger in text_lower for trigger in ["show tasks", "list tasks", "get tasks"]):
        tasks = get_tasks_tool()
        if not tasks:
            return "No tasks found."
        return render_list([{"title": task.title, "description": task.description} for task in tasks], "tasks")

    if "add note" in text_lower or "create note" in text_lower:
        title, content = _parse_create_note(text)
        note = add_note_tool(title, content)
        return f"Note added: {note.title}"

    if any(trigger in text_lower for trigger in ["show notes", "list notes", "get notes"]):
        notes = get_notes_tool()
        if not notes:
            return "No notes found."
        return render_list([{"title": note.title, "description": note.content} for note in notes], "notes")

    history = get_memory()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in history:
        messages.append({"role": "user", "content": item["user"]})
        messages.append({"role": "assistant", "content": item["assistant"]})
    messages.append({"role": "user", "content": text})

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=messages
    )

    output = response.choices[0].message.content
    add_memory(text, output)
    return output
