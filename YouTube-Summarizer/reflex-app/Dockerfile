FROM python:3.11-slim

RUN apt-get update && apt-get install -y unzip curl && apt-get clean

RUN apt-get update && \
    apt-get install -y build-essential git

WORKDIR /code

COPY ./reflex-app/requirements-frontend.txt /code/

RUN pip install --no-cache-dir -r requirements-frontend.txt

COPY ./reflex-app/ /code/reflex

WORKDIR /code/reflex/

EXPOSE 3000

CMD ["reflex", "run"]