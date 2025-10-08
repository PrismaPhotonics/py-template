# Contributor Guide

Thank you for your interest in improving this project.
This project is under the [{{cookiecutter.license}} license](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/LICENSE) and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}})
- [{{cookiecutter.license}} license](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/LICENSE)
- [Documentation](https://prismaphotonics.atlassian.net/wiki/spaces/PRISMA/overview)
- [Issue Tracker](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/issues)

## How to report a bug

Report bugs on the [Issue Tracker](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/issues).

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Issue Tracker](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/issues).

## How to set up your development environment

You need Python 3.8+ and the following tools:

- [UV](https://docs.astral.sh/uv/)
- [Nox](https://nox.thea.codes/)

Install UV:

- MacOS / Linux

```console
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Windows

```console
$ powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> **Note**: UV is also available from `brew`, `winget` and other package managers.
> See full installation instructions in [UV installation](https://docs.astral.sh/uv/getting-started/installation/).

Install Nox globally:

```console
$ pip install nox
```

> **Note**: You can install nox in various ways (pip, pipx, uv, uvx,
> homebrew or other package managers). It's up to you. It's important
> that it is available to you as an entry point to run repo management
> commands.

Set up a dev environment:

```console
$ nox -s dev
$ source .venv/bin/activate
```

## Run admin operations on the project

List the available Nox sessions:

```console
$ nox --list-sessions
```

To run specific Nox sessions (=operations).
For example, invoke the unit test suite like this:

```console
$ nox -s tests
```

Unit tests are located in the `tests` directory,
and are written using the [pytest](https://pytest.readthedocs.io/) testing framework.

To run all available operations:

```console
$ nox
```

## How to submit changes

Open a [pull request](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/pulls) to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks, you can invoke a `lint` session in nox:

```console
$ nox -s lint
```
