###########
# BUILDER #
###########

# pull official base image
FROM python:3.11.1-slim-buster as builder

# set work directory
WORKDIR /app

# create the appropriate directories
ENV APP_HOME=/home/app/backend
WORKDIR $APP_HOME

RUN mkdir ./src
COPY ./pyproject.toml $APP_HOME

# install dependencies
RUN pip install --upgrade pip
RUN pip install -e .

RUN addgroup --system app && adduser --system --group app

#########
# FINAL #
#########

# pull official base image
FROM builder as production

COPY ./src/ $APP_HOME/src/

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

