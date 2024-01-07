# syntax=docker/dockerfile:1

FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000