FROM ubuntu:24.10

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential gdal-bin libicu-dev pkg-config python3-dev python3-poetry \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY poetry.lock ./
COPY poetry.toml ./
COPY pyproject.toml ./
RUN poetry install --no-root --no-dev --no-cache
ENV PATH="/usr/src/app/.venv/bin:$PATH"

COPY data/attributes/.gitignore ./data/attributes/.gitignore
COPY data/boundaries/.gitignore ./data/boundaries/.gitignore
COPY data/images/.gitignore ./data/images/.gitignore
COPY data/tables/.gitignore ./data/tables/.gitignore
COPY src ./src

CMD ["python", "-m", "src"]
