# IT Helpdesk Chatbot — Roadmap

Stage-by-stage execution plan.

### Stage 1 — Setup
- [x] Install Ollama
- [x] Pull gemma3:4b model
- [x] `uv init` — creates `pyproject.toml` (project metadata)
- [x] `uv add ollama` — installs the official Ollama client; `.venv/` and `uv.lock` are created automatically
- [x] Test connection to Ollama from Python (`check_ollama.py`) — not named `test_*.py` so pytest won't pick it up later

Structure stays flat (`main.py`, `check_ollama.py`, `pyproject.toml`) — no `src/` package yet, nothing to split.

### Stage 2 — Basic Chatbot (Terminal)
- [ ] Call Ollama API from Python
- [ ] Terminal input, terminal output
- [ ] Implement streaming response (print token by token instead of waiting for full response)
- [ ] Chat loop with conversation history (context carried between messages)
- [ ] Trim history: keep only the last N messages (system prompt always kept) so the conversation never exceeds the model's context window
- [ ] Handle errors: Ollama not running, empty input, API failure
- [ ] Replace `print()` with `loguru` for all logging

All still in `main.py` — still one script, one concern.

### Stage 3 — IT Helpdesk Persona
- [ ] System prompt as IT Helpdesk assistant (HelpBot)
- [ ] Define scope: what IT topics the bot handles (password reset, VPN, printer, network, software install, etc.)
- [ ] Chatbot only answers IT-related questions
- [ ] Politely declines questions outside of IT topics
- [ ] Write `eval_questions.md`: ~15 test questions in 3 groups — in-scope (IT), off-topic (recipes, politics, homework), bypass attempts ("ignore your instructions...")
- [ ] Run each question against the real model, record pass/fail in the same file
- [ ] Tweak the system prompt, re-run, compare — LLM output varies per run, so this is a manual check, not a unit test

### Stage 4 — Code Structure & Quality
- [ ] Split flat `main.py` into a `src/` package: `src/config.py`, `src/chat.py`, `src/prompts.py`
- [ ] Load config with `pydantic-settings` (not hardcoded values) in `src/config.py`
- [ ] Add `.env.example` with the config keys the app expects
- [ ] Add type hints to all functions
- [ ] Add ruff + mypy config to `pyproject.toml`, run both — fix all warnings

### Stage 5 — Testing
- [ ] Add `tests/` package (`conftest.py`, `test_chat.py`) — natural now that logic lives in `src/`
- [ ] Write `pytest` tests for core functions
- [ ] Test cases: Ollama down, empty input, response error, history trimming
- [ ] Off-topic rejection is NOT unit tested — mocking the model only tests the mock; it's covered by `eval_questions.md` (Stage 3)
- [ ] Mock Ollama API responses with `pytest-mock`
- [ ] Run: `pytest tests/ -v`
- [ ] Minimum 70% coverage: `pytest --cov=src tests/`

### Stage 6 — Streamlit UI
- [ ] Web UI with Streamlit
- [ ] Chat interface (chat bubbles)
- [ ] Streaming response in UI (token by token)
- [ ] Sidebar info: model name and message count per session
- [ ] "Clear Conversation" button to reset chat

### Stage 7 — FastAPI REST API
- [ ] REST API endpoint: `POST /chat`
- [ ] Health check: `GET /healthz` — returns 200 if Ollama is reachable, 503 if not (ready for k8s probes later)
- [ ] Request/response with Pydantic models
- [ ] Session management: store conversation history per session (in-memory dict)
- [ ] Session ID in request/response
- [ ] Streaming response via Server-Sent Events (SSE)
- [ ] Automatic API documentation (Swagger UI at `/docs`)
- [ ] Graceful shutdown with `lifespan` context manager
- [ ] Streamlit UI connects to FastAPI instead of calling Ollama directly

### Bonus — Containerize & Deploy (not scoped yet)
- [ ] Dockerfile: package app + production deps only (no ruff/mypy)
- [ ] Try running it in k3d
- [ ] Decide dev vs prod config split (e.g. `OLLAMA_HOST`)

### Bonus — Simple RAG / Grounding (not scoped yet)
- [ ] Collect internal IT FAQ into text/markdown files (dummy data is fine)
- [ ] Pull an embedding model in Ollama (e.g. `nomic-embed-text`)
- [ ] Chunk documents into small pieces
- [ ] Generate embeddings per chunk, store in-memory (list/array + cosine similarity — no vector DB needed yet)
- [ ] Retrieval: embed the user's question, find top-k most similar chunks
- [ ] Inject relevant chunks into the prompt before sending it to the model
- [ ] Compare answers with & without RAG for org-specific questions (check whether hallucination drops)
