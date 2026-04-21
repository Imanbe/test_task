FROM python:3.11-slim as builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev --group bot

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN addgroup --system botgroup && adduser --system --group botuser

COPY --from=builder /app/.venv /app/.venv

COPY ./bot /app/bot

RUN chown -R botuser:botgroup /app
USER botuser

CMD ["python", "-m", "bot.main"]