# Intent Routing

SoulOS classifies a command before choosing a model or tool. The current catalog covers chat, knowledge search, application operations, screen operations, web search, presentation generation, memory, and unknown input.

The classifier normalizes input, compares it against data-driven examples, extracts lightweight entities, and returns an `IntentResult` containing `intent`, `confidence`, `entities`, and `requires_confirmation`.

Destructive intents are never executed solely because a model suggested them. Low-confidence destructive classifications are marked for confirmation, while the tool API separately requires explicit confirmation for destructive registered tools.

The HTTP contract is `POST /api/v1/intents` with `{ "text": "..." }`.
