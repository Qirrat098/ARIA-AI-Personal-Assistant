from typing import Tuple, Sequence


def split_once(text: str, separator: str) -> Tuple[str, str]:
    if separator in text:
        before, after = text.split(separator, 1)
        return before.strip(), after.strip()
    return text.strip(), ""


def render_list(items: Sequence[dict], item_type: str) -> str:
    if not items:
        return f"No {item_type} found."
    lines = []
    for idx, item in enumerate(items, start=1):
        title = item.get("title", "Untitled")
        body = item.get("description") or item.get("content") or ""
        lines.append(f"{idx}. {title} — {body}")
    return "\n".join(lines)
