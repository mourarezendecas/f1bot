FROM python:3.10.18

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY f1services ./f1services

WORKDIR /app