FROM docker.io/python:3.13.6-slim-bookworm@sha256:2b09112b54420d2e3e814f2cbe34e8e54d32b8c5abd4e72e89cda4758fc6400a AS production

ENV UV_VERSION="0.8.13"
ENV PORT="8080"
ENV SECRET="some other value"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY . /app

RUN useradd --create-home appuser
RUN chown -R appuser:appuser /app
USER appuser

RUN uv sync --locked --no-cache

EXPOSE $PORT

CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--log-level", "info", "--port", "8080"]
