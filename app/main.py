import os
import time
import tomllib
from functools import cache
from pathlib import Path
from typing import Annotated

import requests
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response

from app.exposed_value import InfisicalSource, NeverFetchedError

load_dotenv()

GH_TOKEN = os.getenv('GITHUB_TOKEN', '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')

app = FastAPI()


@app.get('/')
def hello(name: str = 'World'):
    return f'Hello, {name}!'


@app.get('/bye')
def bye(name: str = 'World'):
    return f'Goodbye, {name}!'


@cache
def get_exposed_value_source() -> InfisicalSource:
    """Return the one reader shared by every request, so its cache is shared."""
    return InfisicalSource.from_env()


def running_version() -> str:
    """Return APP_VERSION when the image sets it, else the version in pyproject.toml."""
    if version := os.environ.get('APP_VERSION'):
        return version
    pyproject = Path(__file__).resolve().parent.parent / 'pyproject.toml'
    with pyproject.open('rb') as f:
        return tomllib.load(f)['project']['version']


@app.get('/policeducode')
def police_ducode(
    response: Response,
    source: Annotated[InfisicalSource, Depends(get_exposed_value_source)],
) -> dict[str, object]:
    """Serve the Exposed Value (a Planted Leak path, see docs/adr/0001)."""
    try:
        reading = source.fetch()
    except NeverFetchedError as exc:
        raise HTTPException(
            status_code=503,
            detail='The Exposed Value is not available yet',
            headers={'Cache-Control': 'no-store'},
        ) from exc
    response.headers['Cache-Control'] = 'no-store'
    return {
        'value': reading.value,
        'environment': os.environ.get('APP_ENVIRONMENT', 'local'),
        'rotated_at': reading.rotated_at,
        'version': running_version(),
        'stale': reading.stale,
    }


@app.get('/healthcheck')
def healthcheck() -> dict[str, str]:
    return {'status': 'OK'}


TOO_MANY_REQUESTS = 429


@app.get('/external')
def fetch_external_api() -> dict[str, str]:
    """Fetch data from an external API to demonstrate network requests."""
    max_retries = 5
    backoff = 1
    url = 'https://api.github.com/repos/GitGuardian/ggshield'
    headers = {}
    if GH_TOKEN:
        headers['Authorization'] = f'Bearer {GH_TOKEN}'
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == TOO_MANY_REQUESTS:
                time.sleep(backoff)
                backoff *= 2
                continue
            response.raise_for_status()
            return response.json()
        except (requests.ConnectionError, requests.Timeout) as exc:
            if attempt == max_retries - 1:
                raise HTTPException(
                    status_code=500, detail='External API request failed.'
                ) from exc
            time.sleep(backoff)
            backoff *= 2
            continue
    return None
