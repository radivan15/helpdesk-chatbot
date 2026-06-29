# IT Helpdesk Chatbot (Local AI)

An internal IT Helpdesk chatbot — runs **100% locally** using Ollama. No data leaves your machine, free, and fully open source.

---

## Stack

| Component | Technology | Notes |
|---|---|---|
| LLM Runtime | Ollama 0.22.0 | Run AI models locally |
| Language | Python 3.13+ | Backend and chatbot logic |
| Model | llama3 (4.7 GB) | Open source LLM |
| Prototype UI | Streamlit | Quick web UI for testing |
| Production Web | FastAPI | REST API backend |
| Package Manager | uv | Modern replacement for pip + venv |
| Config | pydantic-settings | Type-safe config from environment variables |

---

## Roadmap

### Stage 1 — Setup ✅
- [x] Install Ollama
- [x] Pull llama3 model
- [x] Create Python virtual environment with `uv`
- [x] Install initial dependencies
- [x] Setup project tooling: Justfile, `.pre-commit-config.yaml`, `pyproject.toml` (ruff + mypy config)
- [x] Test connection to Ollama from Python (`test_ollama.py`)

### Stage 2 — Basic Chatbot (Terminal)
- [ ] Call Ollama API from Python
- [ ] Terminal input, terminal output
- [ ] Implement streaming response (print token by token instead of waiting for full response)
- [ ] Chat loop with conversation history (context carried between messages)
- [ ] Handle errors: Ollama not running, empty input, API failure

### Stage 3 — IT Helpdesk Persona
- [ ] System prompt as IT Helpdesk assistant (HelpBot)
- [ ] Define scope: what IT topics the bot handles (password reset, VPN, printer, network, software install, etc.)
- [ ] Chatbot only answers IT-related questions
- [ ] Politely declines questions outside of IT topics
- [ ] Test edge cases: ambiguous questions, attempts to bypass persona

### Stage 4 — Logging & Code Quality
- [ ] Replace `print()` with `loguru` for all logging
- [ ] Add type hints to all functions
- [ ] Load config with `pydantic-settings` (not hardcoded values)
- [ ] Run `ruff` and `mypy` — fix all warnings
- [ ] Structured logging: every log line includes context (e.g. model name, session ID)

### Stage 5 — Testing
- [ ] Write `pytest` tests for core functions
- [ ] Test cases: Ollama down, empty input, response error, off-topic rejection
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
- [ ] Request/response with Pydantic models
- [ ] Session management: store conversation history per session (in-memory dict)
- [ ] Session ID in request/response
- [ ] Streaming response via Server-Sent Events (SSE)
- [ ] Automatic API documentation (Swagger UI at `/docs`)
- [ ] Graceful shutdown with `lifespan` context manager
- [ ] Streamlit UI connects to FastAPI instead of calling Ollama directly

---

## How to Run

### Prerequisites

- [Ollama](https://ollama.com) installed and running
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) installed (`pip install uv`)

### Install

```bash
# Clone the repo
git clone https://github.com/radivan15/helpdesk-chatbot.git
cd helpdesk-chatbot

# Create virtual environment and install dependencies
uv venv
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Create config file
cp .env.example .env
```

### `.env` Configuration

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3
```

### Run

```bash
# Test connection to Ollama
uv run python test_ollama.py

# Run chatbot (terminal)
uv run python main.py

# Run web UI (Streamlit)
uv run streamlit run app.py

# Run REST API (FastAPI)
uv run uvicorn src.api:app --reload

# Run linting and tests
just check
```

---

## Folder Structure

```
helpdesk-chatbot/
├── main.py                 # Terminal chatbot entry point
├── app.py                  # Streamlit web UI
├── test_ollama.py          # Script to test Ollama connection
├── pyproject.toml          # Project config and dependencies
├── uv.lock                 # Lock file (commit to repo)
├── Justfile                # Task runner (lint, test, security, check)
├── .pre-commit-config.yaml # Pre-commit hooks (ruff, mypy)
├── .env                    # Local config (not pushed to GitHub)
├── .env.example            # Config template
├── .gitignore
├── LICENSE
├── README.md
├── src/
│   ├── __init__.py
│   ├── config.py           # pydantic-settings, load .env
│   ├── chat.py             # Core chat logic + conversation history
│   └── prompts.py          # System prompt definitions
└── tests/
    ├── conftest.py
    └── test_chat.py
```

---

## What I Learned

This project was built while actively learning Python after 6 years in SRE — bridging infrastructure knowledge into code.

### Python Concepts
- **HTTP API calls** with `httpx` — same concept as `curl` health checks I used in SRE, now written in code
- **Streaming responses** — reading tokens as they arrive, similar to tailing logs with `kubectl logs -f`
- **Conversation history as a list** — similar to how a message queue accumulates events, but in memory
- **System prompts** — behaves like a runbook: defines how the bot should respond, what it handles, and what to refuse
- **Type hints** — closer to strongly-typed languages I understand from reading Go; makes Python code more predictable
- **`loguru`** — replaces scattered `print()` statements with structured logs, the same discipline I applied with CloudWatch and Loki
- **`pydantic-settings`** — config management from env vars with type validation, like a strongly-typed version of `os.getenv()`

### Error Handling
- Learned that Python's `try/except` is specific — catching broad `Exception` hides real problems, same lesson as silencing alerts in production
- Handling dependency failures (Ollama down) reminded me of circuit-breaker patterns from SRE

### Project Structure
- `uv` as a package manager is closer to what I expected from modern tooling — lock files, deterministic installs, no virtualenv juggling
- Separating terminal chatbot from web UI early made it easier to test logic without a browser

### Testing
- `pytest` table-driven tests are the Python equivalent of what Go calls test tables — same mental model, different syntax
- Writing tests for "Ollama down" scenario felt natural — in SRE, you always test what happens when a dependency fails
- Mocking external APIs with `pytest-mock` — isolate tests from real Ollama, same principle as stubbing external services in integration tests

### FastAPI
- REST API with auto-generated Swagger docs was the clearest example of why type hints matter — Pydantic uses them to validate input automatically
- Session management in a stateless API — understanding why you need session IDs when HTTP has no memory
- Graceful shutdown with `lifespan` — same concept as SIGTERM handling in Go services

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Notes

- This project is for learning Python while building internal tools
- All models run locally — no data is sent to the cloud
- The chatbot uses the llama3 model via Ollama; can be swapped for other models as needed
