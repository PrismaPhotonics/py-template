{%- macro heading(text) -%}
# {{text}}
{%- endmacro -%}
{{ heading(cookiecutter.friendly_name) }}

[![Tests](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/workflows/Tests/badge.svg)](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/branch/main/graph/badge.svg)](https://app.codecov.io/gh/{{cookiecutter.github_user}}/{{cookiecutter.project_name}})
[![Release](https://github.com/PrismaPhotonics/test-package/workflows/Release/badge.svg)](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/actions?workflow=Release)
[![Secret Scanning](https://github.com/PrismaPhotonics/test-package/workflows/Secret%20Scanning/badge.svg)](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/actions?workflow=Secret%20Scanning)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/charliermarsh/ruff)

## Features

* TODO

## Requirements

* TODO

## Installation

You can install *{{cookiecutter.friendly_name}}* via [pip](https://pip.pypa.io/) from [AWS CodeArtifact](https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure-pip.html):

```console
$ aws codeartifact login --tool pip --domain DOMAIN --domain-owner 111122223333 --repository {{cookiecutter.project_name}}
$ pip install {{cookiecutter.project_name}}
```

## Usage

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide](CONTRIBUTING.md).

## License

Distributed under the terms of the [{{cookiecutter.license.replace("-", " ")}} license](https://opensource.org/licenses/{{cookiecutter.license}}),
*{{cookiecutter.friendly_name}}* is free and open source software.

## Issues

If you encounter any problems,
please [file an issue](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/issues) along with a detailed description.

