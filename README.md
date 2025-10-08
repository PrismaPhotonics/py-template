# py-template

Python template based on [cookiecutter-hypermodern-python](https://cookiecutter-hypermodern-python.readthedocs.io/).

## Usage

```console
$ cruft create https://github.com/PrismaPhotonics/py-template
```

## Features

<!-- features-begin -->

- Fast Python backend with [UV](https://docs.astral.sh/uv/)
- Test automation with [Nox](https://nox.thea.codes/)
- Linting with [pre-commit](https://pre-commit.com/) and [ruff](https://github.com/astral-sh/ruff)
- Continuous integration with [GitHub Actions](https://github.com/features/actions)
- Documentation with Sphinx and [Read the Docs](https://readthedocs.org/) using the furo theme
- Automated uploads to [PyPI](https://pypi.org/)
- Automated dependency updates with [Dependabot](https://dependabot.com/)
- Testing with [pytest](https://docs.pytest.org/en/latest/)
- Code coverage with [Coverage.py](https://coverage.readthedocs.io/)
- Coverage reporting with [Codecov](https://codecov.io/)
- Automated Python syntax upgrades with [pyupgrade](https://github.com/asottile/pyupgrade)
- setuptools as backend, build as frontend

The template supports Python 3.8, 3.9, 3.10 and 3.11.

<!-- features-end -->

## Development

### Running Tests

To test the template itself:

```console
# Install test dependencies
$ pip install -e ".[tests]"

# Run the test suite
$ pytest tests/ -v

# Run with coverage
$ pytest tests/ -v --cov=. --cov-report=html
```

The test suite validates:
- Template generation with cruft
- Project structure and required files
- README and CONTRIBUTING formatting (Markdown)
- CI/CD configuration (GitHub Actions)
- YAML validity of workflow files
- pyproject.toml configuration
- License file generation
- Jinja2 template rendering

