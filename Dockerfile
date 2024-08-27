FROM python:3.12.4-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

