from pathlib import Path

from vylyv_forge.filesystem import create_file
from vylyv_forge.terminal import print_info, print_success


def normalize_requirement(requirement: str) -> str:
    return requirement.strip().lower()


def requirements_file_exists(project_dir: Path) -> bool:
    return (project_dir / "requirements.txt").exists()


def read_requirements(project_dir: Path) -> list[str]:
    requirements_file = project_dir / "requirements.txt"

    if not requirements_file.exists():
        return []

    content = requirements_file.read_text(encoding="utf-8")
    return [line.strip() for line in content.splitlines() if line.strip()]


def write_requirements(project_dir: Path, requirements: list[str]) -> None:
    requirements_file = project_dir / "requirements.txt"
    content = "\n".join(requirements).strip()

    if content:
        content += "\n"

    create_file(requirements_file, content)


def add_requirements_if_missing(
    project_dir: Path,
    dependencies: list[str],
) -> None:
    requirements_file = project_dir / "requirements.txt"

    if not requirements_file.exists():
        print_info("requirements.txt not found. Creating one.")
        create_file(requirements_file, "")

    current_requirements = read_requirements(project_dir)
    normalized_existing = {
        normalize_requirement(requirement)
        for requirement in current_requirements
    }

    added_dependencies: list[str] = []

    for dependency in dependencies:
        normalized_dependency = normalize_requirement(dependency)

        if normalized_dependency not in normalized_existing:
            current_requirements.append(dependency)
            normalized_existing.add(normalized_dependency)
            added_dependencies.append(dependency)

    write_requirements(project_dir, current_requirements)

    if added_dependencies:
        added_text = ", ".join(added_dependencies)
        print_success(f"Updated requirements.txt: {added_text}")
    else:
        print_info("requirements.txt already has the needed dependencies.")