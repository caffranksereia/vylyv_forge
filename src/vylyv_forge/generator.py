import shutil
import sys
from pathlib import Path

from vylyv_forge.errors import ForgeError
from vylyv_forge.process import run_command
from vylyv_forge.templates.api import create_api_template
from vylyv_forge.templates.basic import create_basic_template
from vylyv_forge.templates.saas import create_saas_template
from vylyv_forge.terminal import console, print_info, status
from vylyv_forge.validators import validate_project_name, validate_template


TEMPLATE_BUILDERS = {
    "basic": create_basic_template,
    "api": create_api_template,
    "saas": create_saas_template,
}


def get_venv_python(project_dir: Path) -> Path:
    if sys.platform.startswith("win"):
        return project_dir / ".venv" / "Scripts" / "python.exe"

    return project_dir / ".venv" / "bin" / "python"


def requirements_file_has_content(project_dir: Path) -> bool:
    requirements_file = project_dir / "requirements.txt"

    if not requirements_file.exists():
        return False

    return bool(requirements_file.read_text(encoding="utf-8").strip())


def create_virtual_environment(project_dir: Path) -> Path:
    run_command(
        [sys.executable, "-m", "venv", ".venv"],
        cwd=project_dir,
        error_message="Failed to create virtual environment",
    )

    venv_python = get_venv_python(project_dir)

    if not venv_python.exists():
        raise ForgeError(
            "Virtual environment was created, but Python executable was not found."
        )

    return venv_python


def upgrade_pip(project_dir: Path, venv_python: Path) -> None:
    run_command(
        [str(venv_python), "-m", "pip", "install", "--upgrade", "pip"],
        cwd=project_dir,
        error_message="Failed to upgrade pip",
    )


def install_requirements(project_dir: Path, venv_python: Path) -> None:
    if not requirements_file_has_content(project_dir):
        print_info("No dependencies to install.")
        return

    run_command(
        [str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=project_dir,
        error_message="Failed to install dependencies",
    )


def print_next_steps(name: str, template: str, create_venv: bool) -> None:
    console.print()
    console.print("[bold green]Project created successfully.[/bold green]")
    console.print()
    console.print("[bold]Next commands:[/bold]")
    console.print(f"  [cyan]cd {name}[/cyan]")

    if create_venv:
        if sys.platform.startswith("win"):
            console.print("  [cyan].venv\\Scripts\\activate[/cyan]")
        else:
            console.print("  [cyan]source .venv/bin/activate[/cyan]")

    if template == "basic":
        console.print("  [cyan]python src/main.py[/cyan]")

    elif template == "api":
        console.print("  [cyan]uvicorn src.main:app --reload[/cyan]")

    elif template == "saas":
        console.print("  [cyan]uvicorn src.app:app --reload[/cyan]")


def create_project(
    name: str,
    template: str = "basic",
    create_venv: bool = True,
    install_dependencies: bool = True,
) -> None:
    validate_project_name(name)
    validate_template(template)

    project_dir = Path.cwd() / name

    if project_dir.exists():
        raise ForgeError(f"Folder already exists: {project_dir}")

    template_builder = TEMPLATE_BUILDERS[template]

    print_info(f"Creating project: {name}")
    print_info(f"Template: {template}")

    try:
        project_dir.mkdir(parents=False, exist_ok=False)

        with status("Creating project files"):
            template_builder(project_dir, name)

        if create_venv:
            with status("Creating virtual environment"):
                venv_python = create_virtual_environment(project_dir)

            with status("Upgrading pip"):
                upgrade_pip(project_dir, venv_python)

            if install_dependencies:
                with status("Installing dependencies"):
                    install_requirements(project_dir, venv_python)
            else:
                print_info("Skipping dependency installation.")
        else:
            print_info("Skipping virtual environment creation.")

        print_next_steps(
            name=name,
            template=template,
            create_venv=create_venv,
        )

    except Exception as error:
        if project_dir.exists():
            shutil.rmtree(project_dir, ignore_errors=True)

        if isinstance(error, ForgeError):
            raise error

        raise ForgeError(str(error)) from error