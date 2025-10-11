"""Test suite for validating the py-template cookiecutter template."""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
import yaml


@pytest.fixture(scope="session")
def temp_dir():
    """Create a temporary directory for test projects."""
    tmpdir = tempfile.mkdtemp()
    yield Path(tmpdir)
    shutil.rmtree(tmpdir)


@pytest.fixture(scope="session")
def template_dir():
    """Get the path to the template directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def generated_project(temp_dir, template_dir):
    """Generate a test project using cruft with docs enabled."""
    result = subprocess.run(
        [
            "cruft",
            "create",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_dir),
            "--extra-context",
            json.dumps(
                {
                    "project_name": "test-project",
                    "docs": True,
                    "short_description": "A test project",
                }
            ),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        pytest.fail(f"cruft create failed: {result.stderr}\n{result.stdout}")

    project_path = temp_dir / "test-project"
    if not project_path.exists():
        created = list(temp_dir.iterdir())
        pytest.fail(
            f"Generated project directory does not exist at {project_path}. "
            f"Created: {created}"
        )
    return project_path


@pytest.fixture(scope="session")
def generated_project_no_docs(temp_dir, template_dir):
    """Generate a test project without docs."""
    result = subprocess.run(
        [
            "cruft",
            "create",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_dir),
            "--extra-context",
            json.dumps(
                {
                    "project_name": "test-project-nodocs",
                    "docs": False,
                }
            ),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        pytest.fail(f"cruft create failed: {result.stderr}\n{result.stdout}")

    project_path = temp_dir / "test-project-nodocs"
    if not project_path.exists():
        created = list(temp_dir.iterdir())
        pytest.fail(
            f"Generated project directory does not exist at {project_path}. "
            f"Created: {created}"
        )
    return project_path


class TestProjectStructure:
    """Test the basic structure and essential files of generated projects."""

    def test_essential_files_and_structure(self, generated_project):
        """Test that all essential files and directories exist."""
        # Essential files
        essential = [
            "README.md",
            "CONTRIBUTING.md",
            "LICENSE",
            "pyproject.toml",
            "noxfile.py",
            ".cruft.json",
            "src/test_project/__init__.py",
            "tests/__init__.py",
            "tests/test_test_project.py",
            ".github/workflows/tests.yml",
            ".github/workflows/release.yml",
        ]

        for path in essential:
            full_path = generated_project / path
            assert full_path.exists(), f"Essential path {path} does not exist"

    def test_docs_conditional_generation(
        self, generated_project, generated_project_no_docs
    ):
        """Test that docs are included/excluded based on configuration."""
        # With docs enabled
        assert (generated_project / "docs").is_dir()
        assert (generated_project / "mkdocs.yml").is_file()
        assert (generated_project / ".github" / "workflows" / "docs.yml").is_file()

        # With docs disabled
        assert not (generated_project_no_docs / "docs").exists()
        assert not (generated_project_no_docs / "mkdocs.yml").exists()
        assert not (
            generated_project_no_docs / ".github" / "workflows" / "docs.yml"
        ).exists()


class TestMarkdownDocumentation:
    """Test that documentation is properly rendered as Markdown."""

    def test_readme_markdown_format(self, generated_project):
        """Test README.md is valid markdown with correct structure."""
        readme = generated_project / "README.md"
        content = readme.read_text()

        # Verify markdown format
        assert content.startswith(
            "# Test Project"
        ), "README should start with H1 heading"
        assert (
            "[![" in content and "](https://" in content
        ), "README should have badge links"

        # Verify required sections
        required_sections = [
            "## Features",
            "## Installation",
            "## Contributing",
            "## License",
        ]
        for section in required_sections:
            assert section in content, f"README missing section: {section}"

    def test_contributing_markdown_format(self, generated_project):
        """Test CONTRIBUTING.md is valid markdown with correct structure."""
        contributing = generated_project / "CONTRIBUTING.md"
        content = contributing.read_text()

        assert content.startswith("# Contributor Guide")
        assert "```console" in content, "CONTRIBUTING should have console code blocks"

        # Verify key sections exist
        assert "## How to report a bug" in content
        assert "## How to set up your development environment" in content

    def test_no_template_syntax_in_rendered_files(self, generated_project):
        """Test that Jinja2 template syntax is properly rendered in all files."""
        files_to_check = [
            "README.md",
            "CONTRIBUTING.md",
            "pyproject.toml",
        ]

        for file_path in files_to_check:
            content = (generated_project / file_path).read_text()
            assert "{{" not in content, f"{file_path} has unrendered template syntax"
            assert "}}" not in content, f"{file_path} has unrendered template syntax"
            assert "{%" not in content, f"{file_path} has unrendered template syntax"


class TestConfiguration:
    """Test project configuration files."""

    def test_pyproject_toml_essentials(self, generated_project):
        """Test pyproject.toml has essential configuration."""
        pyproject = generated_project / "pyproject.toml"
        content = pyproject.read_text()

        # Essential sections
        assert "[build-system]" in content
        assert "[project]" in content
        assert "setuptools" in content

        # Markdown README reference
        assert 'readme = "README.md"' in content

        # Test dependencies
        assert "pytest" in content

    def test_github_workflows_valid(self, generated_project):
        """Test that all GitHub Actions workflows are valid YAML."""
        workflows_dir = generated_project / ".github" / "workflows"

        for workflow_file in workflows_dir.glob("*.y*ml"):
            with open(workflow_file) as f:
                try:
                    workflow = yaml.safe_load(f)
                    assert "name" in workflow, f"{workflow_file.name} missing 'name'"
                    assert (
                        "jobs" in workflow or "on" in workflow
                    ), f"{workflow_file.name} missing 'jobs' or 'on'"
                except yaml.YAMLError as e:
                    pytest.fail(f"Invalid YAML in {workflow_file.name}: {e}")


class TestCruftIntegration:
    """Test cruft template tracking and updates."""

    def test_cruft_configuration(self, generated_project):
        """Test that cruft tracking is properly configured."""
        cruft_json = generated_project / ".cruft.json"
        assert cruft_json.exists()

        config = json.loads(cruft_json.read_text())
        assert "template" in config
        assert "commit" in config
        assert "context" in config

    def test_cruft_check_works(self, generated_project):
        """Test that cruft check runs successfully."""
        result = subprocess.run(
            ["cruft", "check"],
            cwd=generated_project,
            capture_output=True,
            text=True,
            check=False,
        )

        # Returns 0 if up-to-date, 1 if updates available - both are valid
        assert result.returncode in [0, 1], f"cruft check failed: {result.stderr}"


class TestLicense:
    """Test Copyright license handling."""

    def test_copyright_license(self, generated_project):
        """Test that Copyright license file is properly generated."""
        license_file = generated_project / "LICENSE"
        assert license_file.exists(), "LICENSE file must exist"

        content = license_file.read_text()
        assert len(content) > 50, "LICENSE file should have substantial content"
        assert "Copyright" in content, "LICENSE must contain Copyright notice"

        # Verify pyproject.toml references the license
        pyproject_content = (generated_project / "pyproject.toml").read_text()
        assert 'license = {text = "Copyright"}' in pyproject_content


class TestPythonPackage:
    """Test Python package structure and validity."""

    def test_noxfile_is_valid_python(self, generated_project):
        """Test that noxfile.py has valid Python syntax."""
        noxfile = generated_project / "noxfile.py"

        result = subprocess.run(
            ["python", "-m", "py_compile", str(noxfile)],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"noxfile.py has syntax errors: {result.stderr}"
