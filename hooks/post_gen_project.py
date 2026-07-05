import shutil
from pathlib import Path


if not {{cookiecutter.docs}}:  # noqa: F821
    shutil.rmtree("docs")
    (Path(".github") / "workflows" / "docs.yaml").unlink()
    # MkDocs' default config filename is mkdocs.yml (.yml, not our usual .yaml),
    # so this must stay .yml to match the actual template file.
    Path("mkdocs.yml").unlink()
