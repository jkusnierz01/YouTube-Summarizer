FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y ffmpeg

COPY ../pyproject.toml ../poetry.lock /code/

RUN pip install poetry && \
    poetry install --only fastapi

COPY ./fastapi/app /code/app

WORKDIR /code/app/

CMD ["poetry","run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]


