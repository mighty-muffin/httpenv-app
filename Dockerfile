FROM docker.io/python:3.13.6-bookworm@sha256:4841ea834ffb3418563b01d3f1a322b057182522ddc7e976775564ea38461023 AS builder

ENV UV_VERSION="0.8.13"

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/${UV_VERSION}/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY ./pyproject.toml .

RUN uv sync

FROM docker.io/python:3.13.6-slim-bookworm@sha256:2b09112b54420d2e3e814f2cbe34e8e54d32b8c5abd4e72e89cda4758fc6400a AS production

ENV SECRET="some other value"

RUN useradd --create-home appuser
USER appuser

WORKDIR /app

COPY /app .
COPY --from=builder /app/.venv .venv

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE $PORT

CMD ["uvicorn", "main:app", "--log-level", "info", "--host", "0.0.0.0" , "--port", "8080"]
