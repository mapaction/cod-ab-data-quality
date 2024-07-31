# Development

We use **[Poetry](https://python-poetry.org/)** for package management.
Poetry is production tested dependency management
tool with exact version locking and support
for packaging and virtual environments.

## Installing Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

If necessary, add poetry location to `PATH`

```bash
echo 'export POETRY_HOME="$HOME/.local/bin"' >> ~/.bashrc

echo 'export PATH="$POETRY_HOME:$PATH"' >> ~/.bashrc

. ~/.bashrc
```

test that installation was successful

```bash
poetry --version
```

### Installing dependencies

Before you start developing in this repository,
you will need to install project dependencies and pre-commit Git hooks.

Navigate to the project directory:

```bash
cd cod-ab-data-quality
```

and run

```bash
make .venv hooks
```

or if you do not have `make` on your OS (i.e. Windows), you can run

```bash
# first install all dependencies
poetry install --no-root

# then install Git hooks
poetry run pre-commit install
```

**NOTE:** any new package can be added to the project by running

```bash
poetry add [package-name]
```

### Optional dependancies

[GDAL](https://gdal.org/download.html) is an optional dependancy which enables file
downloading through `ogr2ogr`,
which is quicker and more memory efficient than using `httpx`.
If not installed,
`httpx` and `geopandas` with `pyarrow` will be used to download files.

To ensure that all commands are able to run in the cloud, it's encouraged to install
[Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Environment file

For variables which change between runs, a dotenv file is used.
Use the example file as a starting point to make a copy from.

```bash
cp .env.example .env
```

### Running commands

Most commands can be accessed through `make`.
In particular, `make run` will run all commands of this project in sequence.

Alternatively, `make run` can be run through the Docker command:

```bash
docker compose up --build
```
