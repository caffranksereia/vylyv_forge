import re
from vylyv_forge.errors import ForgeError

AVAILABLE_TEMPLATES = ("basic", "api", "saas")

PROJECT_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-][a-zA-Z0-9_-]*$")

def validate_project_name(name:str) -> None:
    if not name or not  name.strip():
        raise ForgeError("Project name cannot be empty.")
    
    if not PROJECT_NAME_PATTERN.match(name):
        raise ForgeError( "Invalid project name. Use only letters, numbers, hyphen, or underscore. "
            "The project name must start with a letter.")
    

def validate_template(template: str) -> None:
    if template not in AVAILABLE_TEMPLATES:
        available = ", ".join(AVAILABLE_TEMPLATES)
        raise ForgeError(  f"Unknown template: {template}. Available templates: {available}")

