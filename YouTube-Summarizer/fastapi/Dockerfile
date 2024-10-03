FROM python:3.11-slim

WORKDIR /code

COPY ./pyproject.toml ./poetry.lock /code/

RUN pip install poetry && \
    poetry install

RUN apt-get update && apt-get install -y ffmpeg

COPY ./fastapi/app /code/app

WORKDIR /code/app/

EXPOSE 8080

CMD ["poetry","run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]