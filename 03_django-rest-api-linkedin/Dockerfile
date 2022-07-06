FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /django-rest-app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .