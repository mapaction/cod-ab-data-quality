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
	@poetry run python -m pytest

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

run:
	@echo "Running all commands"
	@make metadata
	@make download

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
	@echo " make run       		- Run all commands"
