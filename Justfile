# Lint: ruff check + format check + mypy
lint:
    uv run ruff check .
    uv run ruff format --check .
    uv run mypy .

# Run tests
test:
    uv run pytest tests/ -v

# Security: scan dependencies for vulnerabilities
security:
    uv run pip-audit

# Format: auto-fix lint + format
format:
    uv run ruff check --fix .
    uv run ruff format .

# Run all checks: lint + test + security
check: lint test security
