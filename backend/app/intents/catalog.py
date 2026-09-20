INTENT_CATALOG: dict[str, tuple[str, ...]] = {
    "chat.general": (
        "talk to me",
        "have a conversation",
        "hello",
        "help me understand this",
        "answer this question",
    ),
    "knowledge.search": (
        "explain a concept",
        "what is",
        "tell me about",
        "give me information about",
        "research this topic",
    ),
    "system.open_app": (
        "open application",
        "launch app",
        "start application",
        "open chrome",
        "open notepad",
    ),
    "system.close_app": (
        "close application",
        "quit app",
        "exit application",
        "close chrome",
    ),
    "system.screen": (
        "take a screenshot",
        "capture my screen",
        "show screen",
        "record screen",
    ),
    "web.search": (
        "search the web",
        "search online",
        "look this up online",
        "find this on the internet",
    ),
    "presentation.generate": (
        "create a presentation",
        "make a powerpoint",
        "generate slides",
        "build a ppt",
    ),
    "memory.store": (
        "remember this",
        "save this to memory",
        "remember that",
    ),
    "memory.retrieve": (
        "what do you remember",
        "recall this from memory",
        "retrieve my memory",
    ),
}

DESTRUCTIVE_INTENTS = {"system.close_app"}
CONFIDENCE_THRESHOLD = 0.52
