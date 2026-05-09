from pathlib import Path

from vylyv_forge.filesystem import create_file, create_init_file


def create_basic_template(project_dir: Path, project_name: str) -> None:
    create_file(
        project_dir / "README.md",
        f"""# {project_name}

Created with Vylyv Forge.

## Run

```bash
python src/main.py
```
""",
    )

    create_file(
        project_dir / ".gitignore",
        """.venv/
__pycache__/
*.pyc
.env
.env.local
""",
    )

    create_init_file(project_dir / "src")

    create_file(
        project_dir / "src" / "main.py",
        """def main() -> None:
    print("Hello from Vylyv Forge!")


if __name__ == "__main__":
    main()
""",
    )

    create_file(
        project_dir / "requirements.txt",
        "",
    )

    create_init_file(project_dir / "tests")

    create_file(
        project_dir / "tests" / "test_main.py",
        """def test_example() -> None:
    assert True
""",
    )