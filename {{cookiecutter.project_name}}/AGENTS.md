# Agent Guide

Guidance for working on **{{ cookiecutter.friendly_name }}**, a Python project.

## Project layout

- `src/{{ cookiecutter.package_name }}/` — the package source code.
- `tests/` — the test suite (pytest).
- `pyproject.toml` — project metadata and tool configuration (ruff, pytest,
  coverage).
- `.pre-commit-config.yaml` — pre-commit hooks (ruff, ruff-format, codespell,
  file/formatting checks).
- `noxfile.py` — task automation entry points.
- `.github/workflows/` — CI (tests, release, semgrep, secret scanning{% if cookiecutter.docs %}, docs{% endif %}).

## Environment

This project uses [uv](https://docs.astral.sh/uv/) for environments and installs,
and [nox](https://nox.thea.codes/) as the task runner.

Set up a development environment:

```console
$ nox -s dev
$ source .venv/bin/activate
```

## Tasks

Run tasks via nox (`nox --list-sessions` shows everything available):

- `nox -s tests` — run the test suite with coverage (pytest) across all
  supported Python versions; use e.g. `nox -s tests-3.12 -- -k <expr>` for a
  single version/subset.
- `nox -s lint` — run all pre-commit checks (ruff lint, formatting, codespell, …).
- `nox -s fmt` — apply ruff formatting.
- `nox -s build` — build the distribution and check it with twine.
{%- if cookiecutter.docs %}
- `nox -s docs` — build the documentation with mkdocs.
{%- endif %}
- `nox -s semgrep-fast` / `nox -s semgrep-all` — run security scans.

## Conventions

- Ruff is configured with `select = ["ALL"]` in `pyproject.toml`; keep the code
  compliant rather than adding blanket ignores.
- Tests live in `tests/` and use pytest; maintain coverage for new code.
- Type hints are expected (ruff `ANN` rules are enabled via `select = ["ALL"]`).

## Workflow rules

- After making changes, **always run `nox -s lint`** and fix every issue it
  reports. Repeat the loop (edit, re-run `nox -s lint`) until it passes cleanly.
- Run `nox -s tests` before finishing to make sure the suite still passes.
