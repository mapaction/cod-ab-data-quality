## Development

We use **[Poetry](https://python-poetry.org/)** for package management. Poetry is production tested dependency management tool with exact version locking and support for packaging and virtual environments.

### Installing Poetry

:book: [Install Poetry on Linux, macOS, Windows (WSL)](https://python-poetry.org/docs/#installing-with-the-official-installer) using the official installer

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

if necessary, add poetry location to `PATH`

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

navigate to the project directory

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

### Lint and format

All code is formatted according to [black](https://black.readthedocs.io/en/stable/), [flake8](https://flake8.pycqa.org/en/latest/), and [PyMarkdown](https://github.com/jackdewinter/pymarkdown) guidelines.  
The repo is set-up to trigger lint tests automatically on each commit using [pre-commit](https://pre-commit.com/).

You can also run lint tests manually using

```bash
make lint
```

or if you do not have `make` on your OS (i.e. Windows), you can run

```bash
poetry run pre-commit run --all-files
```

This is especially useful if you try to resolve some failed test.  
Once you passed all tests, you should see something like this

```bash
$ make lint
Running lint tests..
black....................................................................Passed
isort....................................................................Passed
flake8...................................................................Passed
pymarkdown...............................................................Passed
```
