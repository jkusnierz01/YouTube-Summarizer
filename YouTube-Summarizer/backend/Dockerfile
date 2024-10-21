FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y build-essential g++ git ffmpeg

WORKDIR /code

COPY ./backend/requirements-backend.txt /code/

RUN pip install --no-cache-dir -r requirements-backend.txt

COPY ./backend/app /code/app

WORKDIR /code/app/

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]