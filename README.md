# IT Helpdesk Chatbot (Local AI)

An internal IT Helpdesk chatbot — runs **100% locally** using Ollama. No data leaves your machine, free, and fully open source.

---

## Stack

| Component | Technology | Notes |
|---|---|---|
| LLM Runtime | Ollama 0.22.0 | Run AI models locally |
| Language | Python 3.11+ | Backend and chatbot logic |
| Model | llama3 (4.7 GB) | Open source LLM |
| Prototype UI | Streamlit | Quick web UI for testing |
| Production Web | FastAPI | REST API backend |
| Package Manager | uv | Modern replacement for pip + venv |
| Config | python-dotenv | Environment variable management |

---

## Roadmap

### Stage 1 — Setup
- [ ] Install Ollama
- [ ] Pull llama3 model
- [ ] Create Python virtual environment with `uv`
- [ ] Install initial dependencies
- [ ] Test connection to Ollama from Python (`test_ollama.py`)

### Stage 2 — Basic Chatbot (Terminal)
- [ ] Call Ollama API from Python
- [ ] Terminal input, terminal output
- [ ] Chat loop with conversation history (context carried between messages)
- [ ] Handle errors: Ollama not running, empty input, API failure

### Stage 3 — IT Helpdesk Persona
- [ ] System prompt as IT Helpdesk assistant (HelpBot)
- [ ] Chatbot only answers IT-related questions
- [ ] Politely declines questions outside of IT topics

### Stage 4 — Logging & Code Quality
- [ ] Replace `print()` with `loguru` for all logging
- [ ] Add type hints to all functions
- [ ] Run `ruff` and `mypy` — fix all warnings
- [ ] Structured logging: every log line includes context (e.g. model name, session ID)

### Stage 5 — Testing
- [ ] Write `pytest` tests for core functions
- [ ] Test cases: Ollama down, empty input, response error
- [ ] Run: `pytest tests/ -v`
- [ ] Minimum 70% coverage: `pytest --cov=src tests/`

### Stage 6 — Streamlit UI
- [ ] Web UI with Streamlit
- [ ] Chat interface (chat bubbles)
- [ ] Sidebar info: model name and message count per session
- [ ] "Clear Conversation" button to reset chat

### Stage 7 — FastAPI REST API
- [ ] REST API endpoint: `POST /chat`
- [ ] Request/response with Pydantic models
- [ ] Automatic API documentation (Swagger UI at `/docs`)
- [ ] Streamlit UI connects to FastAPI instead of calling Ollama directly

---

## How to Run

### Prerequisites

- [Ollama](https://ollama.com) installed and running
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) installed (`pip install uv`)

### Install

```bash
# Clone the repo
git clone https://github.com/radivan15/helpdesk-chatbot.git
cd helpdesk-chatbot

# Create virtual environment and install dependencies
uv venv
uv sync

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
uv run python chatbot.py

# Run web UI (Streamlit)
uv run streamlit run app.py

# Run REST API (FastAPI)
uv run uvicorn main:app --reload
```

---

## Folder Structure

```
chatbot-helpdesk-python/
├── chatbot.py          # Terminal chatbot with IT Helpdesk persona
├── app.py              # Web UI with Streamlit
├── main.py             # FastAPI REST API
├── test_ollama.py      # Script to test Ollama connection
├── tests/
│   └── test_chatbot.py # pytest unit tests
├── pyproject.toml      # Project config and dependencies
├── uv.lock             # Lock file (commit to repo)
├── .env                # Local config (not pushed to GitHub)
├── .env.example        # Config template
└── .gitignore
```

---

## What I Learned

This project was built while actively learning Python after 6 years in SRE — bridging infrastructure knowledge into code.

### Python Concepts
- **HTTP API calls** with `requests` — same concept as `curl` health checks I used in SRE, now written in code
- **Conversation history as a list** — similar to how a message queue accumulates events, but in memory
- **System prompts** — behaves like a runbook: defines how the bot should respond, what it handles, and what to refuse
- **Type hints** — closer to strongly-typed languages I understand from reading Go; makes Python code more predictable
- **`loguru`** — replaces scattered `print()` statements with structured logs, the same discipline I applied with CloudWatch and Loki

### Error Handling
- Learned that Python's `try/except` is specific — catching broad `Exception` hides real problems, same lesson as silencing alerts in production
- Handling dependency failures (Ollama down) reminded me of circuit-breaker patterns from SRE

### Project Structure
- `uv` as a package manager is closer to what I expected from modern tooling — lock files, deterministic installs, no virtualenv juggling
- Separating terminal chatbot from web UI early made it easier to test logic without a browser

### Testing
- `pytest` table-driven tests are the Python equivalent of what Go calls test tables — same mental model, different syntax
- Writing tests for "Ollama down" scenario felt natural — in SRE, you always test what happens when a dependency fails

### FastAPI
- REST API with auto-generated Swagger docs was the clearest example of why type hints matter — Pydantic uses them to validate input automatically

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Notes

- This project is for learning Python while building internal tools
- All models run locally — no data is sent to the cloud
- The chatbot uses the llama3 model via Ollama; can be swapped for other models as needed
