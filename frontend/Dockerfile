# syntax=docker/dockerfile:1
ARG POETRY_VERSION=1.8.3
ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim-bookworm
ARG POETRY_VERSION

ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app

COPY pyproject.toml poetry.lock README.md /app/
RUN poetry install --no-interaction --only main --no-root

COPY src /app/src

RUN poetry install --only main

EXPOSE 80
EXPOSE 50051

CMD ["uvicorn", "locallibrary_frontend.web:app", "--host", "0.0.0.0", "--port", "80"]
