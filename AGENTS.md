# Agent Guide

This repository is a [cookiecutter](https://cookiecutter.readthedocs.io/) /
[cruft](https://cruft.github.io/cruft/) **Python project template**. It is not an
application itself: it generates Python projects.

## Layout

- `{{cookiecutter.project_name}}/` — the template of the generated project. Files
  here are rendered with Jinja and may contain `{{ ... }}` / `{% ... %}` syntax.
- `cookiecutter.json` — the template variables and their defaults.
- `hooks/` — pre/post generation hooks that run during `cruft create`.
- `tests/test_template.py` — the template test suite (generates projects with
  `cruft` and asserts on the output).

## Tooling

- Top-level source (`hooks/`, `tests/`) is linted and tested.
- The `{{cookiecutter.project_name}}/` tree is **excluded from ruff** (see
  `extend-exclude` in `pyproject.toml`) because it contains Jinja, not valid
  Python/TOML/YAML until rendered.

## Workflow rules

- After making changes, **always run `nox -s lint`** and fix every issue it
  reports. Repeat the loop (edit, re-run `nox -s lint`) until it passes cleanly.
- Run `nox -s tests` (pytest) to verify template generation still works.
- When editing files under `{{cookiecutter.project_name}}/`, keep the Jinja
  valid and make sure `nox -s tests` still passes — the suite renders the
  template with `cruft` and checks the generated project.
