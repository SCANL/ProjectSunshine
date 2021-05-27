# syntax=docker/dockerfile:1

FROM python:3.7

MAINTAINER Anthony Peruma "axp6201@rit.edu"

RUN mkdir app

WORKDIR /app

RUN mkdir app

WORKDIR /app/app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY src/ .

WORKDIR /app

ENV PYTHONPATH /app/

CMD ["python", "app/main.py"]

