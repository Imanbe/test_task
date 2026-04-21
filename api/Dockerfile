FROM python:3.11-slim as builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --group api

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --system appgroup && adduser --system --group appuser

COPY --from=builder /app/.venv /app/.venv

COPY ./api /app/api
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic
COPY ./api/start.sh /app/start.sh

RUN chmod +x /app/start.sh && chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

CMD ["/app/start.sh"]