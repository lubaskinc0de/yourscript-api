# Contributing to this project

## Preparing the working environment

### 1. Install the uv

#### This project is designed to work with the python package manager called [uv](https://github.com/astral-sh/uv), let's [install it](https://github.com/astral-sh/uv?tab=readme-ov-file#getting-started)

### 2. Making venv

```shell
uv venv
```

### 3. Activating venv

```shell
# On macOS and Linux.
source .venv/bin/activate

# On Windows.
.venv\Scripts\activate
```

### 4. Installing project in development mode

```shell
uv pip install -e .[dev]
```

## Running tests

```shell
pytest tests
```

## Running linters

### Typecheck:
```shell
mypy src/zametka/access_service
```

### Lint
```shell
ruff check
```

### Format
```shell
ruff format
```