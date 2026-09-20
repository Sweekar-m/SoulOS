# SoulOS Desktop Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform SoulOS from a PyQt5/Flask hybrid into a professional cross-platform AI desktop application built with Tauri 2 + React + TypeScript, with FastAPI, NLP intent routing, NVIDIA NIM, modular tools, and a documented API.

**Architecture:** Tauri 2 owns the native desktop shell and OS integration. React/TypeScript provides the desktop UI. A local FastAPI service owns orchestration, NLP intent detection, LLM routing, memory, and tool execution. NVIDIA NIM is the primary generation provider, while deterministic system operations remain behind explicit tool APIs.

**Tech Stack:** Tauri 2, Rust, React, TypeScript, Vite, Tailwind CSS, Framer Motion, FastAPI, Pydantic, Python 3.12+, scikit-learn, httpx, NVIDIA NIM/OpenAI-compatible API, Redis where background work is required, pytest, Vitest, Playwright/Tauri test tooling.

**Spec:** Approved SoulOS desktop architecture discussed in the conversation immediately preceding this plan.

## Global Constraints

- SoulOS is a desktop application, not a web application packaged as the primary product.
- PyQt5/PyQt6 and the existing PyQt startup path must be removed.
- React/TypeScript must run inside Tauri 2 as the primary UI.
- FastAPI must expose versioned `/api/v1/*` endpoints.
- Intent classification must happen before model/tool selection for supported command categories.
- NVIDIA NIM is the primary LLM generation gateway for chat and information generation.
- Tool execution must be explicit, validated, observable, and isolated from raw LLM output.
- Secrets must not be committed; provide `.env.example` and safe configuration loading.
- Existing useful capabilities such as web search, screen capture/streaming, application launching, PPT generation, memory, and the multi-LLM routing concept must be preserved or reimplemented behind the new architecture.
- Every implementation task must end with a focused test cycle and a logical commit.

## Review Focus

1. Ambiguous natural-language commands must not trigger destructive system tools without sufficient intent confidence; test low-confidence routing and confirmation behavior in the intent engine.
2. Malformed or hostile tool arguments must be rejected before OS execution; test schema validation and command allowlists in the tool runtime.
3. NVIDIA NIM outages/timeouts must degrade cleanly; test provider timeout, HTTP failure, malformed response, and health reporting in the LLM gateway.
4. Tauri/frontend/backend version or origin mismatches must surface as actionable errors; test API health/bootstrap and desktop startup paths.
5. Sensitive configuration and access codes must never be exposed through API responses or logs; test redaction and repository configuration hygiene.

---

### Task 1: Establish the New Repository Structure and Configuration

**Files:**
- Create: `backend/app/__init__.py`
- Create: `backend/app/main.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/api/v1/router.py`
- Create: `backend/tests/test_health.py`
- Create: `apps/desktop/package.json`
- Create: `apps/desktop/vite.config.ts`
- Create: `apps/desktop/tsconfig.json`
- Create: `apps/desktop/src/main.tsx`
- Create: `apps/desktop/src/App.tsx`
- Create: `apps/desktop/src-tauri/tauri.conf.json`
- Create: `apps/desktop/src-tauri/src/main.rs`
- Create: `.env.example`
- Modify: `.gitignore`

**Interfaces:**
- Backend exposes `GET /api/v1/health` returning `{ "status": "ok", "service": "souls-backend", "version": string }`.
- Desktop bootstrap targets the local FastAPI service through a configurable API base URL.

- [ ] **Step 1: Write the health endpoint test** using FastAPI `TestClient`, asserting status 200 and the documented response shape.
- [ ] **Step 2: Run the focused test** with `pytest backend/tests/test_health.py -q`; verify it fails before implementation.
- [ ] **Step 3: Implement configuration, FastAPI app factory, and versioned router.** Keep configuration environment-driven and do not load committed secrets.
- [ ] **Step 4: Scaffold the Tauri 2 React application** with Vite and a minimal boot screen that calls `/api/v1/health`.
- [ ] **Step 5: Run backend and frontend checks** and verify the Tauri development shell starts with the React UI.
- [ ] **Step 6: Commit** `chore: scaffold SoulOS desktop architecture`.

### Task 2: Build the NLP Intent Engine

**Files:**
- Create: `backend/app/intents/models.py`
- Create: `backend/app/intents/catalog.py`
- Create: `backend/app/intents/classifier.py`
- Create: `backend/app/intents/entities.py`
- Create: `backend/app/intents/service.py`
- Create: `backend/tests/intents/test_classifier.py`
- Create: `backend/tests/intents/test_entities.py`
- Modify: `backend/app/api/v1/router.py`

**Interfaces:**
- `IntentResult` contains `intent`, `confidence`, `entities`, and `requires_confirmation`.
- `IntentService.classify(text: str) -> IntentResult`.
- Initial intent families: `chat.general`, `knowledge.search`, `system.open_app`, `system.close_app`, `system.screen`, `web.search`, `presentation.generate`, `memory.store`, `memory.retrieve`, and `unknown`.
- `POST /api/v1/intents` accepts `{ "text": string }` and returns `IntentResult`.

- [ ] **Step 1: Add failing tests** for exact matches, paraphrases, unknown input, entity extraction, and low-confidence confirmation.
- [ ] **Step 2: Run the intent tests** and confirm failure.
- [ ] **Step 3: Implement a deterministic first-stage classifier using normalized text, TF-IDF/cosine similarity, intent examples, and lightweight entity extraction.** Keep the catalog data-driven so new intents can be added without changing routing logic.
- [ ] **Step 4: Add the `/api/v1/intents` endpoint.** Validate empty/oversized input and return structured errors.
- [ ] **Step 5: Run intent tests and API tests.**
- [ ] **Step 6: Commit** `feat: add NLP intent routing engine`.

### Task 3: Implement the NVIDIA NIM Gateway and LLM Router

**Files:**
- Create: `backend/app/llm/models.py`
- Create: `backend/app/llm/nim_client.py`
- Create: `backend/app/llm/router.py`
- Create: `backend/app/llm/prompts.py`
- Create: `backend/tests/llm/test_nim_client.py`
- Create: `backend/tests/llm/test_router.py`
- Modify: `backend/app/core/config.py`

**Interfaces:**
- `NimClient.chat(messages, model, temperature, max_tokens)` returns normalized assistant output and provider metadata.
- `LlmRouter.route(intent: IntentResult, context: dict) -> ModelRoute`.
- `GET /api/v1/models` lists configured models without exposing credentials.
- `GET /api/v1/models/health` reports provider availability.

- [ ] **Step 1: Write mocked NIM client tests** for successful generation, timeout, HTTP error, malformed response, and missing credentials.
- [ ] **Step 2: Implement an OpenAI-compatible NIM client using `httpx`, with explicit timeouts and response validation.** Do not hard-code model IDs; configure them through environment variables.
- [ ] **Step 3: Implement intent-aware model routing.** General chat and information generation default to the configured NVIDIA NIM model; specialist models can be selected by intent configuration.
- [ ] **Step 4: Add model listing and health endpoints.**
- [ ] **Step 5: Run all LLM tests with mocked network calls.**
- [ ] **Step 6: Commit** `feat: add NVIDIA NIM gateway and model routing`.

### Task 4: Build the Tool Runtime and API Surface

**Files:**
- Create: `backend/app/tools/base.py`
- Create: `backend/app/tools/registry.py`
- Create: `backend/app/tools/schemas.py`
- Create: `backend/app/tools/system.py`
- Create: `backend/app/tools/search.py`
- Create: `backend/app/tools/presentation.py`
- Create: `backend/app/api/v1/chat.py`
- Create: `backend/app/api/v1/tools.py`
- Create: `backend/app/api/v1/system.py`
- Create: `backend/app/api/v1/search.py`
- Create: `backend/app/api/v1/generate.py`
- Create: `backend/tests/tools/test_registry.py`
- Create: `backend/tests/api/test_chat.py`
- Create: `backend/tests/api/test_tools.py`
- Modify: `backend/app/api/v1/router.py`

**Interfaces:**
- `Tool.execute(arguments: dict) -> ToolResult`.
- `ToolRegistry.get(name: str) -> Tool`.
- `POST /api/v1/chat` accepts `{ "message": string, "session_id": optional string }` and returns intent, route, response, and tool events.
- `POST /api/v1/chat/stream` provides streamed assistant events.
- `GET /api/v1/tools` lists safe tool metadata.
- `POST /api/v1/tools/execute` executes a registered tool after schema validation and authorization/confirmation checks.
- `GET /api/v1/system/apps` and `POST /api/v1/system/apps/open` expose controlled application operations.
- `GET /api/v1/search` performs web-search abstraction.
- `POST /api/v1/generate/presentation` invokes the presentation tool through validated input.

- [ ] **Step 1: Write registry and API tests** covering unknown tools, invalid arguments, low-confidence destructive actions, and successful safe actions.
- [ ] **Step 2: Implement typed tool contracts and a registry.** LLM output must never be executed directly; only registered tool names and Pydantic-validated arguments can reach execution.
- [ ] **Step 3: Port existing SoulOS capabilities** from `tools/` into adapters under the new runtime, preserving behavior while removing direct Flask/PyQt coupling.
- [ ] **Step 4: Implement chat orchestration:** normalize input → classify intent → select tool/model → execute or generate → return structured events.
- [ ] **Step 5: Add API routes and streaming support.**
- [ ] **Step 6: Run API/tool tests.**
- [ ] **Step 7: Commit** `feat: add modular tool runtime and API surface`.

### Task 5: Add Memory and Session Services

**Files:**
- Create: `backend/app/memory/models.py`
- Create: `backend/app/memory/service.py`
- Create: `backend/app/sessions/service.py`
- Create: `backend/tests/memory/test_memory.py`
- Create: `backend/tests/sessions/test_sessions.py`
- Modify: `backend/app/api/v1/router.py`

**Interfaces:**
- `MemoryService.store(session_id, key, value)`.
- `MemoryService.retrieve(session_id, query)`.
- `GET/POST /api/v1/memory/*` and `GET/POST /api/v1/sessions/*` use stable JSON contracts.

- [ ] **Step 1: Write tests** for storing, retrieving, isolation between sessions, and missing records.
- [ ] **Step 2: Implement a simple local persistence layer first** so the desktop app works without a mandatory external database.
- [ ] **Step 3: Integrate memory context into chat orchestration.**
- [ ] **Step 4: Run tests.**
- [ ] **Step 5: Commit** `feat: add local memory and session services`.

### Task 6: Build the Professional Desktop UI

**Files:**
- Create: `apps/desktop/src/components/AppShell.tsx`
- Create: `apps/desktop/src/components/Sidebar.tsx`
- Create: `apps/desktop/src/components/ChatView.tsx`
- Create: `apps/desktop/src/components/CommandPalette.tsx`
- Create: `apps/desktop/src/components/ToolActivity.tsx`
- Create: `apps/desktop/src/components/SystemStatus.tsx`
- Create: `apps/desktop/src/components/ModelSelector.tsx`
- Create: `apps/desktop/src/components/Settings.tsx`
- Create: `apps/desktop/src/lib/api.ts`
- Create: `apps/desktop/src/lib/types.ts`
- Create: `apps/desktop/src/hooks/useChat.ts`
- Create: `apps/desktop/src/styles/globals.css`
- Create: `apps/desktop/src/__tests__/AppShell.test.tsx`
- Modify: `apps/desktop/src/App.tsx`

**Interfaces:**
- `api.chat(message, sessionId)` consumes the backend chat contract.
- UI renders assistant text, intent, tool activity, model information, errors, and connection state.

- [ ] **Step 1: Write component tests** for shell navigation, chat submission, loading/error states, and tool activity rendering.
- [ ] **Step 2: Implement the desktop shell** with sidebar navigation, command palette, chat workspace, activity panel, status indicator, model selector, and settings.
- [ ] **Step 3: Add responsive desktop window behavior and keyboard shortcuts.**
- [ ] **Step 4: Add Framer Motion transitions and a consistent Tailwind design system.** Avoid building a website-like marketing page; the UI should look and behave like an installed productivity application.
- [ ] **Step 5: Connect the UI to FastAPI and streamed chat events.**
- [ ] **Step 6: Run Vitest and Tauri development smoke test.**
- [ ] **Step 7: Commit** `feat: build SoulOS desktop interface`.

### Task 7: Replace the Legacy Runtime and Remove PyQt

**Files:**
- Delete: `frontend/softwareUI.py`
- Delete: `main.py`
- Delete: `flask_app.py`
- Delete: `frontend/code_store.py` if its responsibility is replaced by secure configuration/session services
- Delete: `templates/index.html`
- Delete: legacy Flask/SocketIO-only dependencies from `requirements.txt`
- Delete: PyQt-specific frontend assets that are no longer referenced
- Modify: `requirements.txt` or replace with `backend/pyproject.toml`
- Modify: `.gitignore`

**Interfaces:**
- No production entry point imports PyQt5, Flask, Flask-SocketIO, or the old `frontend.softwareUI` module.

- [ ] **Step 1: Search the repository** for `PyQt5`, `PyQt6`, `QApplication`, `Flask`, `SocketIO`, `softwareUI`, and old entry-point imports.
- [ ] **Step 2: Remove legacy files only after their capabilities have been ported and covered by new tests.**
- [ ] **Step 3: Update dependencies** to the new FastAPI/Tauri architecture.
- [ ] **Step 4: Run a repository-wide static search** and fail the migration if obsolete PyQt imports remain in production code.
- [ ] **Step 5: Run backend and frontend test suites.**
- [ ] **Step 6: Commit** `refactor: remove legacy PyQt and Flask runtime`.

### Task 8: Security, Configuration, and Packaging

**Files:**
- Create: `backend/app/core/security.py`
- Create: `backend/tests/security/test_config.py`
- Create: `apps/desktop/src-tauri/capabilities/default.json`
- Create: `.github/workflows/ci.yml`
- Modify: `.env.example`
- Modify: `.gitignore`
- Modify: `apps/desktop/src-tauri/tauri.conf.json`

**Interfaces:**
- Sensitive settings are loaded only from environment/configuration stores.
- Tauri capabilities explicitly grant only required native permissions.

- [ ] **Step 1: Add tests** that verify secret values are not returned by status/model endpoints and that missing credentials produce safe configuration errors.
- [ ] **Step 2: Implement redaction and strict configuration validation.**
- [ ] **Step 3: Restrict Tauri capabilities** to the desktop operations actually used by SoulOS.
- [ ] **Step 4: Add CI for Python tests, frontend tests, TypeScript checks, and build validation.**
- [ ] **Step 5: Run the full local verification suite.**
- [ ] **Step 6: Commit** `ci: harden SoulOS configuration and desktop packaging`.

### Task 9: Documentation and Migration Guide

**Files:**
- Modify: `README.md`
- Create: `docs/architecture.md`
- Create: `docs/api-reference.md`
- Create: `docs/intent-routing.md`
- Create: `docs/nvidia-nim.md`
- Create: `docs/desktop-development.md`
- Create: `docs/migration-from-pyqt.md`

**Interfaces:**
- Documentation must describe the actual commands, environment variables, API routes, architecture, and desktop development workflow implemented by Tasks 1–8.

- [ ] **Step 1: Document installation and development commands.**
- [ ] **Step 2: Document architecture and data flow with Mermaid diagrams.**
- [ ] **Step 3: Document all versioned API endpoints and example request/response bodies.**
- [ ] **Step 4: Document NLP intent routing and NIM configuration.**
- [ ] **Step 5: Document the PyQt-to-Tauri migration.**
- [ ] **Step 6: Run documentation link/code-block checks where practical.**
- [ ] **Step 7: Commit** `docs: document SoulOS desktop architecture`.

### Task 10: Final Integration and Verification

**Files:**
- Modify: affected files only after verification findings
- Test: `backend/tests/`, `apps/desktop/src/**/*.test.tsx`, Tauri build

- [ ] **Step 1: Run backend tests** with `pytest -q`.
- [ ] **Step 2: Run frontend tests** with the configured package-manager test command.
- [ ] **Step 3: Run TypeScript/build checks** and fix all errors.
- [ ] **Step 4: Run a Tauri desktop development smoke test** covering startup, health connection, chat, intent classification, tool execution, and graceful NIM failure.
- [ ] **Step 5: Verify the repository contains no accidental secrets, `.env` credentials, generated caches, or obsolete PyQt production imports.**
- [ ] **Step 6: Review the complete diff and commit any final fixes** with focused messages.
- [ ] **Step 7: Produce a final migration summary** listing commits, implemented capabilities, tests run, known limitations, and how to launch SoulOS.
