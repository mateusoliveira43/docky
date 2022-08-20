# Docky :whale: + :snake:

[![Continuos Integration](https://github.com/mateusoliveira43/docky/actions/workflows/ci.yml/badge.svg)](https://github.com/mateusoliveira43/docky/actions)
[![Continuos Delivery](https://github.com/mateusoliveira43/docky/actions/workflows/cd.yml/badge.svg)](https://github.com/mateusoliveira43/docky/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Docky: Run Docker commands with Python.

Check the project's documentation [here](https://mateusoliveira43.github.io/docky/).

## Requirements

To run the project, it is necessary the following tools:

- [Python](https://wiki.python.org/moin/BeginnersGuide/Download) 3.7 or higher
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Usage

To get script help, run
```
./scripts/docky.py
./scripts/docky.py <command> --help
```

To connect to container's shell, run
```
./scripts/docky.py run
```
To exit the container's shell, run `CTRL+D` or `exit`.

TODO To run Dockerfile linter, run
```
./scripts/docky.py lint
```

To remove the project's containers, networks, images and volumes, run
```
./scripts/docky.py down
```

To change containers, images and volumes configuration, change the variables in `.env` file.

Run the commands presented in the following sections in the container.

## Quality

The quality metrics of the project are reproduced by the continuos integration (CI) pipeline of the project. CI configuration in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) file.

### Tests

To run tests and coverage report, run
```
pytest
```

To see the html report, check `tests/coverage-results/htmlcov/index.html`.

Tests and coverage configuration in [`pyproject.toml`](pyproject.toml) file.

### Type checking

To run Python type checker, run
```
mypy .
```

Python type checker configuration in [`pyproject.toml`](pyproject.toml) file.

### Linter

To run Python linter, run
```
prospector
prospector --profile tests/.prospector.yaml tests
```

Python linter configuration in [`.prospector.yaml`](.prospector.yaml) and [`tests/.prospector.yaml`](tests/.prospector.yaml)files.

### Code formatters

To check Python code imports format, run
```
isort --check --diff .
```

To format Python code imports, run
```
isort .
```

To check Python code format, run
```
black --check --diff .
```

To format Python code, run
```
black .
```

isort and black configuration in [`pyproject.toml`](pyproject.toml) file.

To check all repository's files format, run
```
ec -verbose
```

File format configuration in [`.editorconfig`](.editorconfig) file.

### Security vulnerability scanners

To check common security issues in Python code, run
```
bandit --recursive scripts/docky_cli
```

To check known security vulnerabilities in Python dependencies, run
```
safety check --file requirements/dev.txt --full-report
```

### Documentation

To check Python documentation generation, run
```
sphinx-apidoc --module-first --private --output-dir docs/modules scripts/docky_cli
sphinx-build -W -T -v -n docs public
```

To generate Python documentation, run
```
sphinx-apidoc --module-first --private --output-dir docs/modules scripts/docky_cli
sphinx-build -v -n docs public
```
To see the documentation , check `public/index.html`.

Sphinx configuration in [`docs/conf.py`](docs/conf.py) file.

The documentation is updated automatically by the continuous deploy (CD) pipeline of the project. CD configuration in [`.github/workflows/cd.yml`](.github/workflows/cd.yml) file.

### Pre-commit

To configure pre-commit automatically when cloning this repo, run
```
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir --hook-type commit-msg --hook-type pre-commit ~/.git-template
```
pre-commit must be installed globally.

To configure pre-commit locally, run
```
pre-commit install --hook-type commit-msg --hook-type pre-commit
```

To test it, run
```
pre-commit run --all-files
```

pre-commit configuration in [`.pre-commit-config.yaml`](.pre-commit-config.yaml) file.

## Update requirements

To update requirements files, run
```
poetry export --format requirements.txt --output requirements/dev.txt --dev
```

## License

This repository is licensed under the terms of [MIT License](LICENSE).

