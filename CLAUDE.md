# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a Python project template using `uv` for dependency management. It includes:

1. A Python package (`testblank`) with simple functionality
2. A Streamlit web application for a ticker-tape calculator
3. Configuration for testing, documentation, and CI/CD

## Development Environment Setup

Set up the development environment with:

```bash
make install
```

This installs dependencies and pre-commit hooks using `uv`.

## Common Commands

### Running the Streamlit App

```bash
streamlit run app.py
```

### Testing

Run all tests:
```bash
uv run pytest
```

Run with coverage:
```bash
uv run pytest --cov=testblank
```

Run a specific test:
```bash
uv run pytest tests/test_foo.py -v
```

### Linting and Formatting

Run all pre-commit hooks:
```bash
uv run pre-commit run -a
```

Run specific linting tools:
```bash
uv run ruff check .
uv run ruff format .
uv run mypy testblank
```

### Documentation

Build documentation:
```bash
uv run mkdocs build
```

Serve documentation locally:
```bash
uv run mkdocs serve
```

## Project Structure

- `testblank/`: Main package directory
  - `__init__.py`: Package initialization
  - `foo.py`: Simple example function

- `tests/`: Test directory
  - `test_foo.py`: Tests for the foo module

- `app.py`: Streamlit ticker-tape calculator application

- Configuration files:
  - `pyproject.toml`: Project metadata and tool configuration
  - `tox.ini`: Multi-environment testing configuration
  - `mkdocs.yml`: Documentation configuration
  - `.pre-commit-config.yaml`: Pre-commit hooks configuration

## Dependency Management

This project uses `uv` for dependency management. Key dependency groups:

- Core dependencies: None currently specified
- Development dependencies: pytest, pre-commit, tox-uv, mypy, ruff, mkdocs, etc.

Add new dependencies by updating the `pyproject.toml` file.

## Release Process

1. Create an API Token on PyPI
2. Add the token to GitHub secrets as `PYPI_TOKEN`
3. Create a new release on GitHub with a tag in the form `*.*.*`

The CI/CD pipeline will automatically build and publish the package to PyPI.

## Streamlit Application

The repository includes a Streamlit application (`app.py`) that implements a ticker-tape calculator with:

- Numeric keypad interface (0-9, decimal point)
- Operation buttons (+, -, ×, ÷)
- Support for multi-step calculations
- Ticker-tape history display
- Operation rollback functionality
- Styled interface with custom CSS

Run the app with `streamlit run app.py`.