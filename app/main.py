import os
import requests
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException


load_dotenv()

SECRET = os.getenv("SECRET", "123456")
GH_TOKEN = os.getenv("GITHUB_TOKEN", "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")

app = FastAPI()


@app.get("/")
def hello(name: str = "World"):
    return f"Hello, {name}!"


@app.get("/bye")
def bye(name: str = "World"):
    return f"Goodbye, {name}!"


@app.get("/policeducode")
def police_ducode(name: str = "SECRET"):
    return f"The secret is... {SECRET}!"


@app.get("/healthcheck")
def healthcheck() -> dict[str, str]:
    return {"status": "OK"}


@app.get("/external")
def fetch_external_api():
    """Fetch data from an external API to demonstrate network requests."""
    max_retries = 5
    backoff = 1
    url = "https://api.github.com/repos/GitGuardian/ggshield"
    headers = {}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 429:
                time.sleep(backoff)
                backoff *= 2
                continue
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            if attempt == max_retries - 1:
                raise HTTPException(status_code=500, detail="External API request failed.")
            time.sleep(backoff)
            backoff *= 2
