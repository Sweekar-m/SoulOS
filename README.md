# soulOS

SoulOS is a cross-platform AI desktop application built around Tauri 2, React/TypeScript, and a local FastAPI orchestration service. The desktop shell owns native integration while the backend handles intent routing, NVIDIA NIM generation, explicit tool execution, memory, and sessions.

## Architecture

- Tauri 2 + React/TypeScript — primary desktop application
- FastAPI — versioned `/api/v1/*` orchestration API
- Intent engine — classification before model/tool selection
- NVIDIA NIM — primary generation gateway
- Typed tool registry — validated, observable, confirmation-aware execution
- Local memory/session services — desktop-friendly state without mandatory external infrastructure

## Development

Backend:

```bash
python -m pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

Desktop:

```bash
cd apps/desktop
npm install
npm run dev
```

Checks:

```bash
python -m pytest backend/tests -q
cd apps/desktop && npm run build && npm test
```

The desktop client defaults to `http://127.0.0.1:8000/api/v1` and can be configured with `VITE_SOULOS_API_URL`. NVIDIA NIM credentials are environment-only.

See `docs/architecture.md`, `docs/api-reference.md`, and `docs/intent-routing.md` for the current implementation contracts.
