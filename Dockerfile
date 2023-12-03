FROM python:3.11-alpine

WORKDIR /app

COPY ./req.txt .

RUN pip install --upgrade pip setuptools

RUN pip install -r req.txt

COPY . .