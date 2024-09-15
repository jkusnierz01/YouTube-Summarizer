FROM ghcr.io/ggerganov/llama.cpp:server

WORKDIR /code

RUN apt-install wget