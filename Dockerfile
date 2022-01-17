# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

RUN apt update
RUN apt install -y git
RUN apt upgrade

RUN python3 -m pip install --upgrade pip google-cloud-bigquery

WORKDIR /packages

COPY ./requirements.txt ./
COPY ./packages/load_datawarehouse ./load_datawarehouse

RUN python3 -m pip install -r requirements.txt

WORKDIR /app

COPY ./app/ ./
COPY ./credentials ./credentials

ENV DOCKER_IMAGE_NAME=bigquery_bbc

# Substitute with your own json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/api-key.json

# Save log to somewhere else
VOLUME ["/log"]

ENTRYPOINT [ "python3", "app.py" ]