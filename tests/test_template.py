"""Test suite for validating the py-template cookiecutter template."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
import yaml


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test projects."""
    tmpdir = tempfile.mkdtemp()
    yield Path(tmpdir)
    shutil.rmtree(tmpdir)


@pytest.fixture
def template_dir():
    """Get the path to the template directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def generated_project(temp_dir, template_dir):
    """Generate a test project using cruft."""
    # Create test project configuration
    project_config = {
        "project_name": "test-project",
        "package_name": "test_project",
        "friendly_name": "Test Project",
        "author": "Test Author",
        "email": "test@example.com",
        "github_user": "TestUser",
        "version": "0.1.0",
        "license": "Copyright",
        "docs": True,
        "short_description": "A test project",
        "development_status": "Development Status :: 3 - Alpha",
    }
    
    # Write config to temp file
    config_file = temp_dir / "config.json"
    config_file.write_text(json.dumps(project_config))
    
    # Run cruft create with config
    result = subprocess.run(
        [
            "cruft",
            "create",
            str(template_dir),
            "--no-input",
            "--config-file",
            str(config_file),
            "--output-dir",
            str(temp_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    
    if result.returncode != 0:
        pytest.fail(f"cruft create failed: {result.stderr}")
    
    project_path = temp_dir / "test-project"
    assert project_path.exists(), "Generated project directory does not exist"
    return project_path


@pytest.fixture
def generated_project_no_docs(temp_dir, template_dir):
    """Generate a test project without docs using cruft."""
    project_config = {
        "project_name": "test-project-nodocs",
        "package_name": "test_project_nodocs",
        "friendly_name": "Test Project No Docs",
        "author": "Test Author",
        "email": "test@example.com",
        "github_user": "TestUser",
        "version": "0.1.0",
        "license": "MIT",
        "docs": False,
        "short_description": "A test project without docs",
        "development_status": "Development Status :: 4 - Beta",
    }
    
    config_file = temp_dir / "config_nodocs.json"
    config_file.write_text(json.dumps(project_config))
    
    result = subprocess.run(
        [
            "cruft",
            "create",
            str(template_dir),
            "--no-input",
            "--config-file",
            str(config_file),
            "--output-dir",
            str(temp_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    
    if result.returncode != 0:
        pytest.fail(f"cruft create failed: {result.stderr}")
    
    project_path = temp_dir / "test-project-nodocs"
    assert project_path.exists(), "Generated project directory does not exist"
    return project_path


class TestProjectStructure:
    """Test the basic structure of generated projects."""

    def test_required_files_exist(self, generated_project):
        """Test that all required files are present."""
        required_files = [
            "README.md",
            "CONTRIBUTING.md",
            "pyproject.toml",
            "noxfile.py",
            ".cruft.json",
            "src/test_project/__init__.py",
            "tests/__init__.py",
            "tests/test_test_project.py",
        ]
        
        for file_path in required_files:
            full_path = generated_project / file_path
            assert full_path.exists(), f"Required file {file_path} does not exist"

    def test_required_directories_exist(self, generated_project):
        """Test that all required directories are present."""
        required_dirs = [
            "src",
            "src/test_project",
            "tests",
            ".github",
            ".github/workflows",
        ]
        
        for dir_path in required_dirs:
            full_path = generated_project / dir_path
            assert full_path.is_dir(), f"Required directory {dir_path} does not exist"

    def test_docs_exist_when_enabled(self, generated_project):
        """Test that docs files exist when docs are enabled."""
        assert (generated_project / "docs").is_dir()
        assert (generated_project / "mkdocs.yml").is_file()
        assert (generated_project / "docs" / "index.md").is_file()
        assert (generated_project / "docs" / "gen_ref_pages.py").is_file()

    def test_docs_absent_when_disabled(self, generated_project_no_docs):
        """Test that docs files are removed when docs are disabled."""
        assert not (generated_project_no_docs / "docs").exists()
        assert not (generated_project_no_docs / "mkdocs.yml").exists()
        assert not (generated_project_no_docs / ".github" / "workflows" / "docs.yml").exists()

    def test_license_file_created(self, generated_project):
        """Test that LICENSE file is created."""
        license_file = generated_project / "LICENSE"
        assert license_file.exists(), "LICENSE file does not exist"


class TestReadmeFormatting:
    """Test README.md formatting and content."""

    def test_readme_is_markdown(self, generated_project):
        """Test that README is markdown format."""
        readme = generated_project / "README.md"
        assert readme.exists()
        content = readme.read_text()
        
        # Check for markdown heading
        assert content.startswith("# Test Project")
        
        # Check for markdown badges (should contain links)
        assert "[![" in content
        assert "](https://" in content

    def test_readme_has_required_sections(self, generated_project):
        """Test that README has all required sections."""
        readme = generated_project / "README.md"
        content = readme.read_text()
        
        required_sections = [
            "## Features",
            "## Requirements",
            "## Installation",
            "## Usage",
            "## Contributing",
            "## License",
            "## Issues",
        ]
        
        for section in required_sections:
            assert section in content, f"README missing section: {section}"

    def test_readme_has_badges(self, generated_project):
        """Test that README includes CI badges."""
        readme = generated_project / "README.md"
        content = readme.read_text()
        
        # Check for various badges
        assert "Tests" in content
        assert "Codecov" in content
        assert "pre-commit" in content

    def test_readme_no_jinja_syntax_left(self, generated_project):
        """Test that no Jinja2 syntax remains in README."""
        readme = generated_project / "README.md"
        content = readme.read_text()
        
        # Check that no template syntax remains
        assert "{{" not in content
        assert "}}" not in content
        assert "{%" not in content
        assert "%}" not in content

    def test_readme_has_correct_project_name(self, generated_project):
        """Test that README contains the correct project name."""
        readme = generated_project / "README.md"
        content = readme.read_text()
        
        assert "Test Project" in content
        assert "test-project" in content


class TestContributingFormatting:
    """Test CONTRIBUTING.md formatting and content."""

    def test_contributing_is_markdown(self, generated_project):
        """Test that CONTRIBUTING is markdown format."""
        contributing = generated_project / "CONTRIBUTING.md"
        assert contributing.exists()
        content = contributing.read_text()
        
        # Check for markdown heading
        assert content.startswith("# Contributor Guide")

    def test_contributing_has_required_sections(self, generated_project):
        """Test that CONTRIBUTING has all required sections."""
        contributing = generated_project / "CONTRIBUTING.md"
        content = contributing.read_text()
        
        required_sections = [
            "## How to report a bug",
            "## How to request a feature",
            "## How to set up your development environment",
            "## Run admin operations on the project",
            "## How to submit changes",
        ]
        
        for section in required_sections:
            assert section in content, f"CONTRIBUTING missing section: {section}"

    def test_contributing_has_code_blocks(self, generated_project):
        """Test that CONTRIBUTING includes code blocks."""
        contributing = generated_project / "CONTRIBUTING.md"
        content = contributing.read_text()
        
        # Check for markdown code blocks
        assert "```console" in content
        assert "```" in content

    def test_contributing_no_jinja_syntax_left(self, generated_project):
        """Test that no Jinja2 syntax remains in CONTRIBUTING."""
        contributing = generated_project / "CONTRIBUTING.md"
        content = contributing.read_text()
        
        # Check that no template syntax remains
        assert "{{" not in content
        assert "}}" not in content
        assert "{%" not in content
        assert "%}" not in content


class TestCIConfiguration:
    """Test GitHub Actions CI configuration."""

    def test_workflows_exist(self, generated_project):
        """Test that required workflow files exist."""
        workflows_dir = generated_project / ".github" / "workflows"
        assert workflows_dir.is_dir()
        
        required_workflows = [
            "tests.yml",
            "release.yml",
            "secret-scanning.yaml",
            "update-template.yaml",
        ]
        
        for workflow in required_workflows:
            workflow_file = workflows_dir / workflow
            assert workflow_file.exists(), f"Workflow {workflow} does not exist"

    def test_docs_workflow_exists_when_enabled(self, generated_project):
        """Test that docs workflow exists when docs are enabled."""
        docs_workflow = generated_project / ".github" / "workflows" / "docs.yml"
        assert docs_workflow.exists()

    def test_workflows_are_valid_yaml(self, generated_project):
        """Test that workflow files are valid YAML."""
        workflows_dir = generated_project / ".github" / "workflows"
        
        for workflow_file in workflows_dir.glob("*.yml"):
            with open(workflow_file) as f:
                try:
                    yaml.safe_load(f)
                except yaml.YAMLError as e:
                    pytest.fail(f"Invalid YAML in {workflow_file.name}: {e}")
        
        for workflow_file in workflows_dir.glob("*.yaml"):
            with open(workflow_file) as f:
                try:
                    yaml.safe_load(f)
                except yaml.YAMLError as e:
                    pytest.fail(f"Invalid YAML in {workflow_file.name}: {e}")

    def test_workflows_have_required_fields(self, generated_project):
        """Test that workflow files have required fields."""
        workflows_dir = generated_project / ".github" / "workflows"
        
        for workflow_file in workflows_dir.glob("*.y*ml"):
            with open(workflow_file) as f:
                workflow = yaml.safe_load(f)
                
                # Check for name field
                assert "name" in workflow, f"{workflow_file.name} missing 'name' field"
                
                # Check for jobs or on field
                assert "jobs" in workflow or "on" in workflow, \
                    f"{workflow_file.name} missing 'jobs' or 'on' field"


class TestPyprojectToml:
    """Test pyproject.toml configuration."""

    def test_pyproject_exists(self, generated_project):
        """Test that pyproject.toml exists."""
        pyproject = generated_project / "pyproject.toml"
        assert pyproject.exists()

    def test_pyproject_has_project_section(self, generated_project):
        """Test that pyproject.toml has [project] section."""
        pyproject = generated_project / "pyproject.toml"
        
        # Read as TOML (using simple parsing since tomllib is Python 3.11+)
        content = pyproject.read_text()
        assert "[project]" in content

    def test_pyproject_has_correct_readme_format(self, generated_project):
        """Test that pyproject.toml references README.md."""
        pyproject = generated_project / "pyproject.toml"
        content = pyproject.read_text()
        
        assert 'readme = "README.md"' in content
        assert 'readme = "README.rst"' not in content

    def test_pyproject_has_build_system(self, generated_project):
        """Test that pyproject.toml has [build-system] section."""
        pyproject = generated_project / "pyproject.toml"
        content = pyproject.read_text()
        
        assert "[build-system]" in content
        assert "setuptools" in content

    def test_pyproject_has_test_dependencies(self, generated_project):
        """Test that pyproject.toml includes test dependencies."""
        pyproject = generated_project / "pyproject.toml"
        content = pyproject.read_text()
        
        assert "pytest" in content
        assert "pytest-cov" in content

    def test_pyproject_no_jinja_syntax_left(self, generated_project):
        """Test that no Jinja2 syntax remains in pyproject.toml."""
        pyproject = generated_project / "pyproject.toml"
        content = pyproject.read_text()
        
        # Check that no template syntax remains
        assert "{{" not in content
        assert "}}" not in content
        assert "{%" not in content
        assert "%}" not in content


class TestDependabotConfiguration:
    """Test Dependabot configuration."""

    def test_dependabot_exists(self, generated_project):
        """Test that dependabot.yml exists."""
        dependabot = generated_project / ".github" / "dependabot.yml"
        assert dependabot.exists()

    def test_dependabot_is_valid_yaml(self, generated_project):
        """Test that dependabot.yml is valid YAML."""
        dependabot = generated_project / ".github" / "dependabot.yml"
        
        with open(dependabot) as f:
            try:
                config = yaml.safe_load(f)
                assert "version" in config
                assert "updates" in config
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML in dependabot.yml: {e}")


class TestCruftConfiguration:
    """Test cruft configuration and template tracking."""

    def test_cruft_json_exists(self, generated_project):
        """Test that .cruft.json exists."""
        cruft_json = generated_project / ".cruft.json"
        assert cruft_json.exists()

    def test_cruft_json_is_valid(self, generated_project):
        """Test that .cruft.json is valid JSON."""
        cruft_json = generated_project / ".cruft.json"
        
        with open(cruft_json) as f:
            try:
                config = json.load(f)
                assert "template" in config
                assert "commit" in config
                assert "context" in config
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in .cruft.json: {e}")

    def test_cruft_update_works(self, generated_project):
        """Test that cruft update can run without errors."""
        result = subprocess.run(
            ["cruft", "check"],
            cwd=generated_project,
            capture_output=True,
            text=True,
            check=False,
        )
        
        # cruft check returns 0 if template is up to date, 1 if not
        # Both are valid states, we just want to ensure it runs without error
        assert result.returncode in [0, 1], f"cruft check failed: {result.stderr}"


class TestPackageStructure:
    """Test Python package structure."""

    def test_package_init_exists(self, generated_project):
        """Test that package __init__.py exists."""
        init_file = generated_project / "src" / "test_project" / "__init__.py"
        assert init_file.exists()

    def test_tests_init_exists(self, generated_project):
        """Test that tests __init__.py exists."""
        init_file = generated_project / "tests" / "__init__.py"
        assert init_file.exists()

    def test_test_file_exists(self, generated_project):
        """Test that test file exists."""
        test_file = generated_project / "tests" / "test_test_project.py"
        assert test_file.exists()

    def test_noxfile_exists(self, generated_project):
        """Test that noxfile.py exists."""
        noxfile = generated_project / "noxfile.py"
        assert noxfile.exists()

    def test_noxfile_is_valid_python(self, generated_project):
        """Test that noxfile.py is valid Python."""
        noxfile = generated_project / "noxfile.py"
        
        result = subprocess.run(
            ["python", "-m", "py_compile", str(noxfile)],
            capture_output=True,
            text=True,
            check=False,
        )
        
        assert result.returncode == 0, f"noxfile.py has syntax errors: {result.stderr}"


class TestLicenseHandling:
    """Test license file handling for different license types."""

    def test_copyright_license_created(self, generated_project):
        """Test that Copyright license file is created."""
        license_file = generated_project / "LICENSE"
        assert license_file.exists()
        content = license_file.read_text()
        assert "Copyright" in content

    def test_mit_license_created(self, generated_project_no_docs):
        """Test that MIT license file is created."""
        license_file = generated_project_no_docs / "LICENSE"
        assert license_file.exists()
        content = license_file.read_text()
        assert "MIT" in content

