# azure_call_direct.py
import os, requests, time, json

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT",)
API_KEY = os.getenv("AZURE_OPENAI_KEY",)
DEPLOYMENT = os.getenv("DEPLOYMENT_NAME",)
API_VER = os.getenv("API_VERSION", )

url = f"{AZURE_ENDPOINT}/openai/deployments/{DEPLOYMENT}/chat/completions?api-version={API_VER}"
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}
payload = {
    "messages":[{"role":"user","content":"Hello from direct POST test"}],
    "temperature":0.2,
    "max_tokens":200
}

def call_with_retry(url, headers, payload, retries=3, timeout=20):
    for attempt in range(1, retries+1):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=timeout)
            print("Attempt", attempt, "status:", r.status_code)
            print(r.text[:1000])
            return r
        except requests.exceptions.ConnectTimeout:
            print(f"Attempt {attempt}: ConnectTimeout")
        except requests.exceptions.ReadTimeout:
            print(f"Attempt {attempt}: ReadTimeout")
        except requests.exceptions.ConnectionError as e:
            print(f"Attempt {attempt}: ConnectionError:", e)
        except Exception as e:
            print("Attempt", attempt, "Other error:", e)
        time.sleep(2 * attempt)  # backoff
    return None

if __name__ == "__main__":
    call_with_retry(url, headers, payload, retries=3, timeout=30)

