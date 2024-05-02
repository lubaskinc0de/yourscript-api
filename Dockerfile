###########
#  BASE   #
###########

FROM python:3.11.1-slim-buster as base

WORKDIR /app

ENV APP_HOME=/home/app/backend
WORKDIR $APP_HOME

RUN mkdir ./src

RUN addgroup --system app && adduser --system --group app

RUN pip install uv

###########
#  VENV   #
###########

FROM base as venv

RUN uv venv

###########
# BUILDER #
###########

FROM venv as builder

COPY ./pyproject.toml $APP_HOME
RUN uv pip install -e .

#########
# FINAL #
#########

FROM builder as production

COPY ./src/ $APP_HOME/src/

RUN chown -R app:app $HOME

USER app

