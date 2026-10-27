import ollama

# kirim pesan ke model
response = ollama.chat(
    model="gemma3:4b",
    messages=[{"role": "user", "content": "say hello in one sentence"}],
)


# balasan ada di response.message.content
print(response.message.content)