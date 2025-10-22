FROM docker.io/python:3.14.0-slim-bookworm@sha256:8a8d3341dfc71b7420256ceff425f64247da7e23fbe3fc23c3ea8cfbad59096d AS production

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
