FROM python:3.12-slim AS builder

ENV UV_CACHE_DIR=/root/.cache/uv \
    UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/

WORKDIR /app

RUN --mount=type=cache,target=$UV_CACHE_DIR \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

ADD . /app

RUN --mount=type=cache,target=$UV_CACHE_DIR \
    uv sync --frozen --no-editable

FROM python:3.12-slim AS runtime

# Add system dependencies installation when needed

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONOTWRITEBYTECODE=1 \
    PYTHONPATH=/src

WORKDIR /src

COPY --from=builder --chown=app:app ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src

RUN useradd --create-home --shell /bin/bash app

COPY --from=builder --chown=app:app ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --chown=app:app src ./src
COPY --chown=app:app .env ./.env

# Switch to app user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/v1/health/ || exit 1

# Start the application
CMD ["uvicorn", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory", "--workers", "4"]
