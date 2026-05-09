from pathlib import Path
import subprocess
import sys
import venv
import shutil

TEMPLATES = {
    "basic": ["ruff", "pytest"],
    "api" : ["fastapi", "uvicorn", "pytest","ruff",],
    "saas" : [
        "fastapi",
        "uvicorn",
        "psycopg2-binary",
        "python-dotenv",
        "pyjwt",
        "bcrypt",
        "ruff",
        "pytest",
    ],
}

BASE_STRUCTURE = {
    "src": ["core", "shared", "modules", "routers"],
    "tests": [],
}

def create_files(project_path: Path, template:str):
    (project_path / "README.md").write_text(
        f"# {project_path.name}\n\nGenerated with Vylyv Forge.\n",
        encoding="utf-8",
    )

    (project_path / ".env.example").write_text(
        f"APP_NAME={project_path.name}\n\n# ENV=development\n",
        encoding="utf-8",
    )
    
    requirements = "\n".join(TEMPLATES[template])
    (project_path / "requirements.txt").write_text(
        requirements,
        encoding="utf-8"
    )

    app_file = project_path / "src" / "app.py"
    app_file.write_text(
        """
        def main():
            print("Vylyv Forge app running...")

        if __name__ == "__main__":
            main()
        """,
        encoding="utf-8"
    )

def create_folders(project_path: Path):
        for folder, subfolders in BASE_STRUCTURE.items():
            base = project_path / folder
            base.mkdir(parents=True, exist_ok=True)

            for sub in subfolders:
                path = base / sub
                path.mkdir(parents=True, exist_ok=True)
                (path / "__init__.py").write_text("", encoding="utf-8")

def create_virtual_env(project_path: Path):
    venv_path = project_path / ".venv"

    print("Creating .venv...")

    venv.create(venv_path, with_pip=True)

    print(f"Virtual environment created at {venv_path}")

def get_pip_path(project_path: Path) -> Path:
        if sys.platform.startswith("win"):
            return project_path / "venv" / "Scripts" / "pip.exe"
       
        return project_path / "venv" / "bin" / "pip"

def install_dependencies(project_path: Path):
    python_path = get_python_path(project_path)
    requirements_path = project_path / "requirements.txt"

    print("Installing dependencies...")

    subprocess.run(
        [
            str(python_path),
            "-m",
            "pip",
            "install",
            "--no-cache-dir",
            "-r",
            str(requirements_path),
        ],
        check=True,
    )


    print("Dependencies installed.")

def init_git(project_path: Path):
        try:
            subprocess.run(["git", "init"], cwd=project_path, check=True)
            print("Git repository initialized.")
        except Exception as e:
            print(f"Error initializing git repository: {e}")
            print("Please ensure git is installed and available in your PATH.")

def create_project(template: str, project_name: str, install: bool, use_git: bool):
    project_path = Path(project_name)

    if project_path.exists():
        print(f"Project '{project_name}' already exists.")
        return

    try:
        project_path.mkdir()

        create_folders(project_path)
        create_files(project_path, template)
        create_virtual_env(project_path)

        if install:
            upgrade_pip(project_path)
            install_dependencies(project_path)

        if use_git:
            init_git(project_path)

        print(f"\nProject '{project_name}' created successfully.")

    except Exception as error:
        print("\nProject creation failed.")
        print(f"Error: {error}")

        if project_path.exists():
            print("Cleaning broken project folder...")
            shutil.rmtree(project_path)

        print("Broken project folder removed.")

def get_python_path(project_path: Path):
    possible_paths = [
        project_path / ".venv" / "Scripts" / "python.exe",
        project_path / ".venv" / "Scripts" / "python",
        project_path / ".venv" / "bin" / "python",
        project_path / ".venv" / "bin" / "python3",
    ]


    for path in possible_paths:
        if path.exists():
            return path
    
    raise FileNotFoundError("Python executable not found inside .venv")

def upgrade_pip(project_path: Path):
    python_path = get_python_path(project_path)

    print(f"Using Python at: {python_path}")
    print("Upgrading pip...")

    subprocess.run(
        [str(python_path), "-m", "pip", "install", "--upgrade", "pip"],
        check=True,
    )

    print("Pip upgraded.")

    