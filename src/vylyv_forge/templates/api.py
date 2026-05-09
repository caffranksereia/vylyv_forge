from pathlib import Path

from vylyv_forge.filesystem import create_file, create_init_file


def create_api_template(project_dir: Path, project_name: str) -> None:
    create_file(
        project_dir / "README.md",
        f"""# {project_name}

API project created with Vylyv Forge.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn src.main:app --reload
```

## Health check

```txt
GET /api/health
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

    folders = [
        "src",
        "src/api",
        "src/core",
        "src/schemas",
        "src/services",
        "tests",
    ]

    for folder in folders:
        create_init_file(project_dir / folder)

    create_file(
        project_dir / "src" / "main.py",
        """from fastapi import FastAPI

from src.api.routes import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(title="Vylyv Forge API")
    app.include_router(api_router)
    return app


app = create_app()
""",
    )

    create_file(
        project_dir / "src" / "api" / "routes.py",
        """from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "API running",
    }
""",
    )

    create_file(
        project_dir / "src" / "core" / "config.py",
        """from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
    app_name: str = getenv("APP_NAME", "Vylyv Forge API")
    app_env: str = getenv("APP_ENV", "development")


settings = Settings()
""",
    )

    create_file(
        project_dir / "src" / "schemas" / "health.py",
        """from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    message: str
""",
    )

    create_file(
        project_dir / "src" / "services" / "health_service.py",
        """def get_health_status() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "API running",
    }
""",
    )

    create_file(
        project_dir / "requirements.txt",
        """fastapi
uvicorn
python-dotenv
pydantic
pytest
httpx
ruff
""",
    )

    create_file(
        project_dir / ".env.example",
        """APP_NAME=Vylyv Forge API
APP_ENV=development
""",
    )

    create_file(
        project_dir / "tests" / "test_health.py",
        """from fastapi.testclient import TestClient

from src.main import app


def test_health_check() -> None:
    client = TestClient(app)

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
""",
    )