import httpx


def chat(message: str, history: list[dict[str, str]]) -> str:
    """Kirim pesan ke Ollama dengan conversation history."""
    history.append({"role": "user", "content": message})

    response = httpx.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3",
            "messages": history,
            "stream": False,
        },
        timeout=60.0,
    )
    response.raise_for_status()

    assistant_message: str = response.json()["message"]["content"]
    history.append({"role": "assistant", "content": assistant_message})
    return assistant_message


def main() -> None:
    """Chat loop — ketik 'exit' untuk keluar."""
    history: list[dict[str, str]] = []
    print("Helpdesk Chatbot (type 'exit' to quit)")  # noqa: T201
    print("=" * 45)  # noqa T201

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Bye!")  # noqa: T201
            break

        if not user_input:
            continue

        answer = chat(user_input, history)
        print(f"\nBot: {answer}")  # noqa: T201


if __name__ == "__main__":
    main()
