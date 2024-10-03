FROM python:3.11-slim

WORKDIR /code

COPY ./pyproject.toml ./poetry.lock /code/

RUN pip install poetry && \
    poetry install

COPY ./reflex-app/ /code/reflex

RUN apt-get update && apt-get install -y unzip curl && apt-get clean

WORKDIR /code/reflex/

EXPOSE 9000

CMD [ "poetry", "run", "reflex", "run", "--frontend-port", "9000" ]