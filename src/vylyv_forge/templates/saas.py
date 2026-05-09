from pathlib import Path

from vylyv_forge.filesystem import create_file, create_folder, create_init_file


def create_saas_template(project_dir: Path, project_name: str) -> None:
    create_file(
        project_dir / "README.md",
        f"""# {project_name}

SaaS backend project created with Vylyv Forge.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn src.app:app --reload
```

## Project structure

```txt
src/
├── app.py
├── core/
├── database/
├── modules/
├── routers/
└── shared/
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
logs/
""",
    )

    folders = [
        "src",
        "src/core",
        "src/core/auth",
        "src/core/config",
        "src/core/security",
        "src/database",
        "src/modules",
        "src/modules/users",
        "src/modules/users/dto",
        "src/modules/users/repository",
        "src/modules/users/service",
        "src/modules/users/validators",
        "src/routers",
        "src/shared",
        "src/shared/dto",
        "src/shared/errors",
        "src/shared/validators",
        "tests",
    ]

    for folder in folders:
        create_init_file(project_dir / folder)

    create_folder(project_dir / "logs")

    create_file(
        project_dir / "src" / "app.py",
        """from fastapi import FastAPI

from src.routers.api_router import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="Vylyv SaaS Backend")
    app.include_router(api_router)
    return app


app = create_app()
""",
    )

    create_file(
        project_dir / "src" / "routers" / "api_router.py",
        """from fastapi import APIRouter

api_router = APIRouter(prefix="/api")


@api_router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "SaaS backend running",
    }
""",
    )

    create_file(
        project_dir / "src" / "core" / "config" / "settings.py",
        """from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Vylyv SaaS"
    app_env: str = "development"

    db_host: str = "localhost"
    db_name: str = "app_db"
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_port: int = 5432

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
""",
    )

    create_file(
        project_dir / "src" / "core" / "auth" / "password.py",
        """import bcrypt


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
""",
    )

    create_file(
        project_dir / "src" / "core" / "auth" / "jwt.py",
        """from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from src.core.config.settings import settings


def create_access_token(data: dict[str, Any], expires_minutes: int = 60) -> str:
    payload = data.copy()

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload.update({"exp": expires_at})

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
""",
    )

    create_file(
        project_dir / "src" / "database" / "connection.py",
        """import psycopg2
from psycopg2.extensions import connection

from src.core.config.settings import settings


def get_connection() -> connection:
    return psycopg2.connect(
        host=settings.db_host,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        port=settings.db_port,
    )
""",
    )

    create_file(
        project_dir / "src" / "shared" / "errors" / "app_error.py",
        """class AppError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
""",
    )

    create_file(
        project_dir / "src" / "shared" / "dto" / "base_response.py",
        """from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    message: str
""",
    )

    create_file(
        project_dir / "src" / "modules" / "users" / "dto" / "create_user_dto.py",
        """from pydantic import BaseModel, EmailStr


class CreateUserDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
""",
    )

    create_file(
        project_dir / "src" / "modules" / "users" / "validators" / "user_validator.py",
        """from src.shared.errors.app_error import AppError


def validate_user_name(name: str) -> None:
    if not name or len(name.strip()) < 3:
        raise AppError("User name must have at least 3 characters.")


def validate_password(password: str) -> None:
    if not password or len(password) < 8:
        raise AppError("Password must have at least 8 characters.")
""",
    )

    create_file(
        project_dir / "src" / "modules" / "users" / "repository" / "user_repository.py",
        '''from src.database.connection import get_connection


def find_user_by_email(email: str) -> dict | None:
    query = """
        SELECT id, name, email
        FROM users
        WHERE email = %s
        LIMIT 1
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (email,))
            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
    }
''',
    )

    create_file(
        project_dir / "src" / "modules" / "users" / "service" / "user_service.py",
        """from src.modules.users.dto.create_user_dto import CreateUserDTO
from src.modules.users.validators.user_validator import (
    validate_password,
    validate_user_name,
)


def create_user(dto: CreateUserDTO) -> dict[str, str]:
    validate_user_name(dto.name)
    validate_password(dto.password)

    return {
        "status": "created",
        "message": "User creation flow is ready to be implemented.",
    }
""",
    )

    create_file(
        project_dir / "requirements.txt",
        """fastapi
uvicorn
python-dotenv
pydantic
pydantic-settings
email-validator
psycopg2-binary
bcrypt
PyJWT
pytest
httpx
ruff
""",
    )

    create_file(
        project_dir / ".env.example",
        """APP_NAME=Vylyv SaaS
APP_ENV=development

DB_HOST=localhost
DB_NAME=app_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432

JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
""",
    )

    create_file(
        project_dir / "tests" / "test_health.py",
        """from fastapi.testclient import TestClient

from src.app import app


def test_health_check() -> None:
    client = TestClient(app)

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
""",
    )