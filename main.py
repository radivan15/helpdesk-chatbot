import ollama

# riwayat percakapan
messages: list[dict[str, str]] = []
# batas jumlah pesan yang disimpan; kecil dulu supaya mudah diuji
MAX_MESSAGES = 6


while True:
    question = input("You: ")
    if question == 'exit':
        break
    
    messages.append({"role": "user", "content": question})
    
    
    stream = ollama.chat(
        model="gemma3:4b",
        messages=messages,
        stream=True,    
    )


    print("Bot: ", end="")
    reply = "" # kumpulkan potongan jadi satu string utuh
    for chunk in stream:
        piece = chunk.message.content
        print(piece, end="", flush=True)
        reply += piece
    print()
    
    # simpan balasan bot, supaya giliran berikutnya model melihatnya
    messages.append({"role": "assistant", "content": reply})
    
    # buang pesan lama (setelah jawaban bot masuk, supaya selalu berpasangan)
    messages = messages[-MAX_MESSAGES:]
    print(len(messages))