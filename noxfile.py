"""Automation using nox."""

import os

import nox
from nox.command import CommandFailed

nox.options.default_venv_backend = "uv|virtualenv"
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["lint", "tests"]


@nox.session(python="3.11")
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
def dev(session: nox.Session) -> None:
    """Set up a python development environment for the project"""
    args = session.posargs or (".venv",)
    venv_dir = os.fsdecode(os.path.abspath(args[0]))

    session.log(f"Setting up virtual environment in {venv_dir}")
    session.run("uv", "venv", "--python", "3.11", venv_dir, silent=True)
    session.install("-e", ".[dev]", env={"VIRTUAL_ENV": venv_dir}, external=True)


@nox.session(name="semgrep-fast")
def semgrep_fast(session):
    """Fast code security + Bandit parity on Python files."""
    try:
        session.run("uv", "pip", "install", "semgrep", silent=True, external=True)
    except CommandFailed:
        session.run("uv", "pip", "install", "semgrep")

    session.run(
        "semgrep",
        "scan",
        "--config=p/python",
        "--config=p/ci",
        "--config=p/bandit",
        "--max-target-bytes=1500000",
        "--severity=ERROR",
        "--error",
        external=True,
    )


@nox.session(name="semgrep-all")
def semgrep_all(session):
    """Run all semgrep security scans in sequence."""
    try:
        session.run("uv", "pip", "install", "semgrep", silent=True, external=True)
    except CommandFailed:
        session.run("uv", "pip", "install", "semgrep")

    # Run all scans
    session.run(
        "semgrep",
        "scan",
        "--config=p/ci",
        "--config=p/python",
        "--config=p/bandit",
        "--config=p/secrets",
        "--config=p/owasp-top-ten",
        "--config=p/security-audit",
        "--max-target-bytes=2000000",
        "--timeout=120",
        "--timeout-threshold=5",
        "--severity=WARNING",
        "--sarif-output=.reports/semgrep.sarif",
        external=True,
    )
