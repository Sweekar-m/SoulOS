# SoulOS API Reference

All application routes are versioned under `/api/v1`.

| Route | Purpose |
|---|---|
| `GET /health` | Backend health and version |
| `GET /models` | Configured model metadata without credentials |
| `GET /models/health` | NVIDIA NIM availability |
| `POST /intents` | Classify a natural-language command |
| `GET /tools` | List registered tool metadata |
| `POST /tools/execute` | Execute a validated registered tool |
| `POST /memory/store` | Store session memory |
| `POST /memory/retrieve` | Retrieve session memory |
| `POST /sessions` | Create a session |
| `GET /sessions/{session_id}` | Fetch a session |
| `GET /conversations/{session_id}` | Fetch conversation history |
| `POST /conversations/{session_id}/messages` | Append a validated conversation message |
| `DELETE /conversations/{session_id}` | Clear conversation history |
| `POST /chat` | Run intent → routing → generation orchestration and persist the conversation |

Conversation history is local to the running service and is scoped by session ID. Tool execution is schema-validated and destructive tools require explicit confirmation. Provider credentials are configuration-only and are not returned by API responses.
