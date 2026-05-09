from typing import Annotated

import typer
from rich.prompt import Confirm, Prompt

from vylyv_forge.errors import ForgeError
from vylyv_forge.generator import create_project
from vylyv_forge.module_generator import create_module
from vylyv_forge.terminal import console, print_error, print_logo


app = typer.Typer(
    name="forge",
    help="Forge - Python project generator.",
    no_args_is_help=False,
    add_completion=False,
)


def ask_template() -> str:
    console.print()
    console.print("[bold]Choose a template:[/bold]")
    console.print("[cyan]1[/cyan] - basic")
    console.print("[cyan]2[/cyan] - api")
    console.print("[cyan]3[/cyan] - saas")

    choices = {
        "1": "basic",
        "2": "api",
        "3": "saas",
        "basic": "basic",
        "api": "api",
        "saas": "saas",
    }

    answer = Prompt.ask(
        "Template",
        choices=list(choices.keys()),
        default="basic",
    )

    return choices[answer]


def create_project_flow(
    name: str | None = None,
    template: str | None = None,
    create_venv: bool | None = None,
    install_dependencies: bool | None = None,
) -> None:
    if name is None:
        name = Prompt.ask("Project name")

    if template is None:
        template = ask_template()

    if create_venv is None:
        create_venv = Confirm.ask(
            "Create virtual environment?",
            default=True,
        )

    if install_dependencies is None:
        if create_venv:
            install_dependencies = Confirm.ask(
                "Install dependencies?",
                default=True,
            )
        else:
            install_dependencies = False

    create_project(
        name=name,
        template=template,
        create_venv=create_venv,
        install_dependencies=install_dependencies,
    )


def create_module_flow(
    name: str | None = None,
    with_router: bool | None = None,
    with_tests: bool | None = None,
    crud: bool | None = None,
    update_requirements: bool | None = None,
) -> None:
    if name is None:
        name = Prompt.ask("Module name")

    if with_router is None:
        with_router = Confirm.ask(
            "Create router?",
            default=True,
        )

    if with_tests is None:
        with_tests = Confirm.ask(
            "Create tests?",
            default=True,
        )

    if crud is None:
        crud = Confirm.ask(
            "Create CRUD starter?",
            default=False,
        )

    if update_requirements is None:
        update_requirements = Confirm.ask(
            "Update requirements.txt?",
            default=True,
        )

    create_module(
        name=name,
        with_router=with_router,
        with_tests=with_tests,
        crud=crud,
        update_requirements=update_requirements,
    )


def show_main_menu() -> None:
    print_logo()

    console.print("[bold]What do you want to do?[/bold]")
    console.print()
    console.print("[cyan]1[/cyan] - Create project")
    console.print("[cyan]2[/cyan] - Create module")
    console.print("[cyan]3[/cyan] - Show help")
    console.print("[cyan]0[/cyan] - Exit")
    console.print()

    choice = Prompt.ask(
        "Choose an option",
        choices=["1", "2", "3", "0"],
        default="1",
    )

    try:
        if choice == "1":
            create_project_flow()
            return

        if choice == "2":
            create_module_flow()
            return

        if choice == "3":
            console.print(app.get_help(ctx=typer.Context(app)))
            return

        console.print("[yellow]Bye.[/yellow]")

    except ForgeError as error:
        print_error(str(error))
        raise typer.Exit(code=1) from error


@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context) -> None:
    """
    Forge CLI.
    """
    if ctx.invoked_subcommand is None:
        show_main_menu()
        raise typer.Exit()


@app.command("create")
def create_command(
    name: Annotated[
        str | None,
        typer.Argument(help="Project name."),
    ] = None,
    template: Annotated[
        str | None,
        typer.Option(
            "--template",
            "-t",
            help="Project template: basic, api, or saas.",
        ),
    ] = None,
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
        create_project_flow(
            name=name,
            template=template,
            create_venv=False if no_venv else None,
            install_dependencies=False if no_install else None,
        )
    except ForgeError as error:
        print_error(str(error))
        raise typer.Exit(code=1) from error


@app.command("module")
def module_command(
    name: Annotated[
        str | None,
        typer.Argument(help="Module name."),
    ] = None,
    with_router: Annotated[
        bool,
        typer.Option(
            "--with-router",
            help="Create router file.",
        ),
    ] = False,
    with_tests: Annotated[
        bool,
        typer.Option(
            "--with-tests",
            help="Create test file.",
        ),
    ] = False,
    crud: Annotated[
        bool,
        typer.Option(
            "--crud",
            help="Create CRUD starter files.",
        ),
    ] = False,
    no_requirements: Annotated[
        bool,
        typer.Option(
            "--no-requirements",
            help="Do not update requirements.txt.",
        ),
    ] = False,
) -> None:
    print_logo()

    try:
        create_module_flow(
            name=name,
            with_router=True if with_router else None,
            with_tests=True if with_tests else None,
            crud=True if crud else None,
            update_requirements=False if no_requirements else None,
        )
    except ForgeError as error:
        print_error(str(error))
        raise typer.Exit(code=1) from error


def main() -> None:
    app()