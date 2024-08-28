FROM python:3.12.4-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    DJANGO_SECRET_KEY='devsecretkey'

RUN apt update && \
    apt install --no-install-recommends -y curl build-essential git locales-all wait-for-it

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN pip install --no-cache-dir --upgrade pip uwsgi

WORKDIR /app

ADD pyproject.toml /app

RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app
