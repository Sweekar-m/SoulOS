import re


APP_PATTERN = re.compile(r"(?:open|launch|start|close|quit|exit)\s+(?:the\s+)?([a-zA-Z0-9._ -]+?)(?:\s+please)?$", re.I)


def extract_entities(text: str, intent: str) -> dict[str, str]:
    entities: dict[str, str] = {}
    if intent in {"system.open_app", "system.close_app"}:
        match = APP_PATTERN.search(text.strip())
        if match:
            entities["application"] = match.group(1).strip()
    return entities
