ARG POETRY_VERSION=1.8.3
# Use the official Python 3.12 bullseye image as the base image
FROM python:3.12-bullseye AS base
ARG POETRY_VERSION

# Set up Poetry
RUN pip install poetry==${POETRY_VERSION} && pip install poetry-plugin-bundle
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock README.md .

# Install the dependencies (without the main project)
RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main --no-root --no-directory --no-interaction

# Bundle the project and its dependencies into /app
COPY src/ ./src/
RUN poetry bundle venv --python=/usr/local/bin/python --only=main /app


# Use the official Python 3.12 slim image as the final image
FROM python:3.12-slim AS final
# Set the working directory
WORKDIR /app

# Copy the bundled application to the working directory and set the permissions
COPY --from=base  /app ./

ENV PATH=/app/bin:$PATH
ENV PYTHONPATH=/app/lib/python3.12/site-packages

# web server port
EXPOSE 80
# gRPC server port
EXPOSE 50051

CMD ["uvicorn", "locallibrary_frontend.web:app", "--host", "0.0.0.0", "--port", "80"]
