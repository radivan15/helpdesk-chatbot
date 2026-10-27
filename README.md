# IT Helpdesk Chatbot (Local AI)

An internal IT Helpdesk chatbot — will run **100% locally** using Ollama. No data will leave your machine, free, and fully open source.

> Status: work in progress

---

## What it does

By the end of this project:

- A chatbot answers common IT helpdesk questions (password resets, VPN access, printer issues, network troubleshooting, software installs) so users get instant answers without waiting for a human
- Everything runs locally via Ollama, so no conversation data leaves the machine and there are no API costs
- The bot stays in its HelpBot persona: it only answers IT topics, politely declines anything else, and its behavior is checked against a written set of eval questions
- Responses stream token by token, and conversation history is trimmed so it never overflows the model's context window
- Failures (Ollama down, empty input, API errors) are handled with clear messages and logged with loguru, not shown as raw tracebacks
- It starts as a terminal chat, grows into a Streamlit web UI, and ends with a FastAPI REST API (`POST /chat`, `GET /healthz`) that the UI talks to
- Code quality is checked with ruff + mypy, and core logic is covered by pytest with mocked Ollama responses

---

## Why I'm building it

Most IT helpdesk tickets — password resets, VPN access, printer issues — are repetitive and could be resolved before ever reaching a human, similar to the L1 triage I've seen in on-call SRE work. This project is a hands-on way to learn LLM integration in Python, while also exploring a "local AI" approach (Ollama) that keeps all data on-device instead of sending it to a third-party API — relevant for environments with strict data-handling requirements.

---

## Stack

| Component | Technology | Notes |
|---|---|---|
| LLM Runtime | Ollama (latest) | Run AI models locally |
| Model | gemma3:4b (3.3 GB) | Open source LLM, lite version |
| LLM Client | `ollama` (official Python library) | Stage 1 |
| Language | Python 3.13+ | Backend and chatbot logic |
| Package Manager | uv | Modern replacement for pip + venv |
| Logging | loguru | Stage 2 |
| Config | pydantic-settings | Type-safe config from environment variables, Stage 4 |
| Linting & formatting | ruff | Stage 4 |
| Type checking | mypy | Stage 4 |
| Testing | pytest + pytest-mock + pytest-cov | Stage 5 |
| Prototype UI | Streamlit | Quick web UI, Stage 6 |
| REST API | FastAPI | API backend for the UI, Stage 7 |

---

## Folder Structure

Flat structure for now (Stage 1). A `src/` package comes in Stage 4.

```
helpdesk-chatbot/
├── check_ollama.py     # smoke test: can Python reach Ollama?
├── main.py             # chatbot entry point (built in Stage 2)
├── pyproject.toml      # project metadata + dependencies
├── uv.lock             # pinned dependency versions
├── .python-version     # Python version used by uv
├── .gitignore
├── LICENSE
├── README.md
└── ROADMAP.md
```

---

## Installation

Prerequisites: [Ollama](https://ollama.com/download) and [uv](https://docs.astral.sh/uv/).

```powershell
# 1. Pull the model
ollama pull gemma3:4b

# 2. Clone the repo and install dependencies (creates .venv from uv.lock)
git clone https://github.com/radivan15/helpdesk-chatbot.git
cd helpdesk-chatbot
uv sync
```

---

## How to Run

Make sure Ollama is running, then check the connection:

```powershell
uv run python check_ollama.py
```

If Ollama is not running, you will get `ConnectionError: Failed to connect to Ollama...`.

The terminal chatbot (`main.py`) will be added in Stage 2.

---

## Roadmap

Detailed execution roadmap is in [ROADMAP.md](ROADMAP.md).

---

## License

MIT License — see [LICENSE](LICENSE)


