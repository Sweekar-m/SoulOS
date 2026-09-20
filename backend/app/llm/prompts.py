DEFAULT_SYSTEM_PROMPT = """You are SoulOS, a local-first desktop AI assistant.
Be concise, factual, and explicit about uncertainty. Never claim a system action
was executed unless a registered tool has actually reported success."""
 

def build_chat_messages(user_message: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
