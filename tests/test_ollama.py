from ollama import Client


def test_ollama_connection():
    client = Client(host="http://localhost:11435")

    response = client.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": "Rispondi solamente con: OK",
            }
        ],
    )

    assert response["message"]["content"].strip() == "OK"