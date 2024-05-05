FROM python:3.11.7

LABEL org.opencontainers.image.source=https://github.com/melhin/just-another-rss-reader

ARG APP_NAME=just-another-rss-reader
ARG APP_PATH=/opt/$APP_NAME
ARG PYTHON_VERSION=3.10.1
ARG POETRY_VERSION=1.1.15

EXPOSE 7000

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_NO_INTERACTION=1
ENV LANG C.UTF-8

# install deps
RUN apt-get update -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install -U pip setuptools wheel poetry
#ENV PATH="$POETRY_HOME/bin:$PATH;"


WORKDIR /code
COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry config virtualenvs.create false
ARG ADD_DEV_DEPS=""
RUN if [ ! -z "$ADD_DEV_DEPS" ]; \
    then \
        poetry install; \
    else \
        poetry install --only main; \
    fi


# Collect static files
COPY . /code
RUN python manage.py collectstatic --noinput
COPY . /code

RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD ["main"]
