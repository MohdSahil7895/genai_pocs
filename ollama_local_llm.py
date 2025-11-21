# main.py
import os
import sys
import requests
import json

OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "kimi-k2-thinking:cloud")

def query_model(prompt: str):
    url = f"{OLLAMA_ENDPOINT}/api/chat"
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.2}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling Ollama: {e}")
    except KeyError:
        raise RuntimeError("Unexpected response format from Ollama")

if __name__ == "__main__":
    try:
        out = query_model("Explain what uv is in simple terms.")
        print("MODEL RESPONSE:\n", out)
    except Exception as e:
        print("Error querying model:", type(e), e)
        sys.exit(1)
