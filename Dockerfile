FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gdal-bin python3-poetry \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY poetry.lock ./
COPY poetry.toml ./
COPY pyproject.toml ./
RUN poetry install --no-root --no-dev --no-cache
ENV PATH="/usr/src/app/.venv/bin:$PATH"

COPY data/boundaries/.gitignore ./data/boundaries/.gitignore
COPY data/images/.gitignore ./data/images/.gitignore
COPY data/reports/.gitignore ./data/reports/.gitignore
COPY data/tables/.gitignore ./data/tables/.gitignore
COPY src ./src

CMD ["python", "-m", "src"]
