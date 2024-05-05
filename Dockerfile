FROM python:3.11.1-slim-buster as base

WORKDIR /app

ENV APP_HOME=/home/app/backend
WORKDIR $APP_HOME

RUN mkdir ./src

RUN addgroup --system app && adduser --system --group app

RUN pip install uv

COPY ./pyproject.toml $APP_HOME

RUN uv pip install -e . --system

COPY ./src/ $APP_HOME/src/

RUN chown -R app:app $HOME

USER app
