FROM python:3.11-slim

WORKDIR /code

COPY ../pyproject.toml ../poetry.lock /code/

RUN pip install poetry && \
    poetry install