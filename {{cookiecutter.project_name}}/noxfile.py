"""Automation using nox."""

import glob
import os

import nox

nox.options.default_venv_backend = "uv|virtualenv"
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["lint", "tests"]


@nox.session(
    python=["3.8", "3.9", "3.10", "3.11", "3.12"],
)
def tests(session: nox.Session) -> None:
    """Run tests using pytest"""
    session.install(".[tests]")
    session.run(
        "pytest",
        "--cov",
        "--cov-config=pyproject.toml",
        *session.posargs,
        env={"COVERAGE_FILE": f".coverage.{session.python}"},
    )


@nox.session
def fmt(session: nox.Session) -> None:
    """Run ruff code formatting"""
    session.install("pre-commit")
    session.install("-e", ".[dev]")
    session.run("pre-commit", "run", "ruff")


@nox.session
def lint(session: nox.Session) -> None:
    """Run all lint checks on the project using pre-commit"""
    session.install("pre-commit")
    session.install("-e", ".[dev]")

    args = *(session.posargs or ("--show-diff-on-failure",)), "--all-files"
    session.run("pre-commit", "run", *args)


@nox.session
def build(session: nox.Session) -> None:
    """Build the python package"""
    session.install("build", "setuptools", "twine")
    session.run("uv", "build")
    dists = glob.glob("dist/*")
    session.run("twine", "check", *dists, silent=True)


@nox.session
def dev(session: nox.Session) -> None:
    """Set up a python development environment for the project"""
    args = session.posargs or (".venv",)
    venv_dir = os.fsdecode(os.path.abspath(args[0]))

    session.log(f"Setting up virtual environment in {venv_dir}")
    session.run("uv", "venv", venv_dir, silent=True)
    session.install("-e", ".[dev]", env={"VIRTUAL_ENV": venv_dir}, external=True)

{% if cookiecutter.docs != "False" -%}
@nox.session
def docs(session: nox.Session) -> None:
    session.install(".[docs]")
    session.run("mkdocs", "build")
{% endif -%}
