# Desktop Integration

The desktop shell is the primary SoulOS runtime. It composes the sidebar, chat view, model catalog, tool activity, settings, and command palette around the versioned FastAPI service.

The client reads `VITE_SOULOS_API_URL` and defaults to `http://127.0.0.1:8000/api/v1`. The active session ID is kept in browser session storage so a reload can recover conversation history from the local service.

Backend health is refreshed periodically. Model metadata is loaded from `GET /api/v1/models`; provider credentials are never exposed to the desktop UI.

Tool events returned by chat are normalized before rendering so malformed provider data cannot directly affect the activity panel.
