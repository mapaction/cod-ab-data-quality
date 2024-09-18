.PHONY: all
all = help

.venv:
	@echo "Installing project dependencies.."
	@poetry install --no-root


hooks:
	@echo "Adding pre-commit hooks.."
	@poetry run pre-commit install


test:
	@echo "Running unit tests.."
	@poetry run pytest

lint:
	@echo "Running lint tests.."
	@poetry run pre-commit run --all-files

clean:
	@echo "Removing .venv"
	@rm -rf .venv
	@poetry env remove --all

metadata:
	@echo "Generating metadata"
	@poetry run python -m src.metadata

download:
	@echo "Downloading boundaries"
	@poetry run python -m src.download

checks:
	@echo "Running checks"
	@poetry run python -m src.checks

scores:
	@echo "Calculating scores"
	@poetry run python -m src.scores

images:
	@echo "Generating reports"
	@poetry run python -m src.images

reports:
	@echo "Generating reports"
	@poetry run python -m src.reports

run:
	@echo "Running all commands"
	@poetry run python -m src

help:
	@echo "Available make targets:"
	@echo " make help           - Print help"
	@echo " make .venv          - Install project dependencies"
	@echo " make hooks          - Add pre-commit hooks"
	@echo " make test           - Run unit tests"
	@echo " make lint           - Run lint tests"
	@echo " make clean          - Remove .venv"
	@echo " make metadata       - Generate metadata"
	@echo " make download       - Download boundaries"
	@echo " make checks       	- Run checks"
	@echo " make scores       	- Calculate scores"
	@echo " make images       	- Generate images"
	@echo " make reports       	- Generate reports"
	@echo " make run       		- Run all commands"
