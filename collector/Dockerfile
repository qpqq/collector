# BASE PYTHON IMAGE
FROM python:3.13.0-slim-bookworm AS base


# BUILD PYTHON
# pull official base image
FROM base AS py_builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# install system dependencies
RUN apt update && \
#    apt install -y --no-install-recommends build-essential && \
    pip install --upgrade pip

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# lint
RUN pip install flake8~=7.1.0
COPY ./source /usr/src/app/
RUN #flake8 --ignore=E501,W504 .  # TODO


# FINAL
# pull official base image
FROM base

# create the app user
RUN groupadd -g 1002 app && \
    useradd app -u 1001 -g 1002

# set enviroment variables
ENV HOME=/home/app \
    APP_HOME=/home/app/collector

# create the appropriate directories
WORKDIR $APP_HOME

# install dependencies
RUN pip install --upgrade pip
COPY --from=py_builder /usr/src/app/wheels ./wheels
RUN pip install --no-cache ./wheels/*

# copy project
COPY ./source ./source

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app
