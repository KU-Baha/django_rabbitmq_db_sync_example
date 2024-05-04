# ---------------------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------------------
FROM python:3.12-slim as base

WORKDIR /app

ENV PYTHONUNBUFFERED 1

# System deps
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    # deps for internationalization and localization
    gettext \
    # deps for multimedia files and streams
    ffmpeg \
    # deps for psycopg2
    libpq-dev \
    python3-dev \
    gcc

# ---------------------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------------------

FROM base as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install Poetry
RUN pip install poetry==1.8.2

COPY ../pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

# ---------------------------------------------------------------------------------------
# Runtime
# ---------------------------------------------------------------------------------------

FROM base as runtime

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ../src /app/src

WORKDIR /app/src

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

COPY docker/queue.sh /queue.sh
RUN chmod +x /queue.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000