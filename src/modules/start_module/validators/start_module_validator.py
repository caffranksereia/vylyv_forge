from src.shared.errors.app_error import AppError


def validate_start_module_name(name: str) -> None:
    if not name or len(name.strip()) < 3:
        raise AppError("Start_Module name must have at least 3 characters.")
