FROM docker.io/python:3.13.7-slim-bookworm@sha256:9b8102b7b3a61db24fe58f335b526173e5aeaaf7d13b2fbfb514e20f84f5e386 AS production

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV UV_VERSION="0.8.13"
ENV PORT="8080"
ENV SECRET="some other value"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY . /app

RUN useradd --create-home appuser
RUN chown -R appuser:appuser /app
USER appuser

RUN uv sync --locked --no-cache --no-dev

EXPOSE $PORT

CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--log-level", "info", "--port", "8080"]
