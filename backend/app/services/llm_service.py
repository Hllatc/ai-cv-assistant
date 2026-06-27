import requests

OLLAMA_URL = "http://ollama:11434/api/generate"

def generate_with_qwen(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]