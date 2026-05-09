from pathlib import Path
 
def create_file(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def create_folder(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def create_init_file(folder: Path) -> None:
    init_file = folder / "__init__.py"
    if not init_file.exists():
        create_file(init_file)