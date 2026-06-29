import httpx


def test_connection() -> None:
    base_url = "http://localhost:11434"

    # cek ollama server
    response = httpx.get(f"{base_url}/api/tags")
    print(f"Status: {response.status_code}")  # noqa: T201

    # list model
    models = response.json()
    for model in models["models"]:
        print(f"Model: {model['name']}")  # noqa: T201


if __name__ == "__main__":
    test_connection()
