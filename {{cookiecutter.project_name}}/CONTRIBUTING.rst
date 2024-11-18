Contributor Guide
=================

Thank you for your interest in improving this project.
-This project is close-source under the `{{cookiecutter.license}} license`_ and
-welcomes contributions in the form of bug reports, feature requests, and pull requests.


Here is a list of important resources for contributors:

- `Source Code`_
- `{{cookiecutter.license}} license`_
- `Documentation`_
- `Issue Tracker`_

.. _Source Code: https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}
.. _`{{cookiecutter.license}} license`: https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/LICENSE
.. _Documentation: https://prismaphotonics.atlassian.net/wiki/spaces/PRISMA/overview
.. _Issue Tracker: https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/issues

How to report a bug
-------------------

Report bugs on the `Issue Tracker`_.

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.


How to request a feature
------------------------

Request features on the `Issue Tracker`_.


How to set up your development environment
------------------------------------------

You need Python 3.8+ and the following tools:

- UV_
- Nox_

Install UV:

- MacOS / Linux

.. code:: console

   $ curl -LsSf https://astral.sh/uv/install.sh | sh

- Windows

.. code:: console

   $ powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

- OSX

.. code:: console

   $ pip install nox

.. note:: UV is also available from `brew`, `winget` and other package managers.
    See full installation instructions in UV_installation_

Install the package with development requirements:

.. code:: console

   $ uv pip install nox

.. _UV: https://docs.astral.sh/uv/
.. _UV_installation: https://docs.astral.sh/uv/getting-started/installation/
.. _Nox: https://nox.thea.codes/

Set up a dev environment:

.. code-block:: console

   $ nox -s dev
   $ source .venv/bin/activate


How to test the project
-----------------------

Run the full test suite:

.. code:: console

   $ nox

List the available Nox sessions:

.. code:: console

   $ nox --list-sessions

You can also run a specific Nox session.
For example, invoke the unit test suite like this:

.. code:: console

   $ nox --session=tests

Unit tests are located in the ``tests`` directory,
and are written using the pytest_ testing framework.

.. _pytest: https://pytest.readthedocs.io/


How to submit changes
---------------------

Open a `pull request`_ to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks, you can invoke a `lint` session in nox:

.. code:: console

   $ nox -s lint

.. _pull request: https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/pulls
.. github-only
