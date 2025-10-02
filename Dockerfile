FROM docker.io/python:3.13.7-slim-bookworm@sha256:adafcc17694d715c905b4c7bebd96907a1fd5cf183395f0ebc4d3428bd22d92d AS production

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
