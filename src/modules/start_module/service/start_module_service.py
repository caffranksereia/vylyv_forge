from src.modules.start_module.dto.create_start_module_dto import CreateStartModuleDTO
from src.modules.start_module.validators.start_module_validator import validate_start_module_name


def create_start_module(dto: CreateStartModuleDTO) -> dict[str, str]:
    validate_start_module_name(dto.name)

    return {
        "status": "created",
        "message": "Start_Module creation flow is ready to be implemented.",
    }
