from enum import Enum
from typing import Annotated

import typer

from vylyv_forge.errors import ForgeError
from vylyv_forge.generator import create_project
from vylyv_forge.terminal import print_error, print_logo


class TemplateOption(str, Enum):
    basic = "basic"
    api = "api"
    saas = "saas"


app = typer.Typer(
    name="forge",
    help="Forge - Python project generator.",
    no_args_is_help=True,
    add_completion=True,
)


@app.command()
def create(
    name: Annotated[
        str,
        typer.Argument(help="Project name."),
    ],
    template: Annotated[
        TemplateOption,
        typer.Option(
            "--template",
            "-t",
            help="Project template.",
        ),
    ] = TemplateOption.basic,
    no_venv: Annotated[
        bool,
        typer.Option(
            "--no-venv",
            help="Do not create a virtual environment.",
        ),
    ] = False,
    no_install: Annotated[
        bool,
        typer.Option(
            "--no-install",
            help="Do not install dependencies from requirements.txt.",
        ),
    ] = False,
) -> None:
    print_logo()

    try:
        create_project(
            name=name,
            template=template.value,
            create_venv=not no_venv,
            install_dependencies=not no_install,
        )
    except ForgeError as error:
        print_error(str(error))
        raise typer.Exit(code=1) from error


def main() -> None:
    app()