FROM python:3.10.6-slim-bullseye

COPY . /app
WORKDIR /app

RUN apt update && apt install -y curl

# Install poetry
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-dev --no-interaction --no-ansi

RUN adduser app
USER app

EXPOSE 8000
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "-t", "300", "main:app"]
