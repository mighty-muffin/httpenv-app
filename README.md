# httpenv-app

A tiny HTTP server built with FastAPI, demonstrating usage of environment variables and modern Python packaging with [UV](https://github.com/astral-sh/uv).

## Features

- Simple HTTP API with endpoints:
  - `/` — returns a greeting
  - `/bye` — returns a farewell
  - `/???` — returns a secret (chuuu don't tell anyone)

## Requirements

- [Python 3.13+](https://docs.python.org/3/whatsnew/3.13.html)
- [UV package manager](https://github.com/astral-sh/uv)
- [Docker buildx](https://docs.docker.com/reference/cli/docker/buildx/)

## Getting Started

### 1. Install UV

Follow instructions from the [UV Docs](https://docs.astral.sh/uv/) or use:

```sh
curl -Ls https://astral.sh/uv/install.sh | sh
uv self version # uv 0.8.13
```

### 2. Setup python & install dependencies

Run the following command in the project directory:

```sh
uv venv --python 3.13
uv sync
uv run pytest # If you want to run the tests
```

### 3. Run the server

Start the FastAPI server using Uvicorn:

```sh
uv run uvicorn app.main:app --port 8080 # Go to http://localhost:8080
```

## Build a container

To build this container run these commands:

```sh
docker buildx build -f Dockerfile . -t httpenv-app
docker run -d httpenv-app:latest
```

## Environment Variables

Rename `.sample.env` to `.env` file in the project root and include a secret var here:

```sh
SECRET ="<your-token-here>"
```
