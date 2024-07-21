FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gdal-bin make python3-poetry python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY poetry.lock ./
COPY poetry.toml ./
COPY pyproject.toml ./
RUN poetry install --no-root

COPY src ./src
COPY tests ./tests
COPY Makefile ./

CMD ["make", "run"]
