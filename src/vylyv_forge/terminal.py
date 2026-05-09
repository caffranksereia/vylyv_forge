from collections.abc import Iterator
from contextlib import contextmanager

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


console = Console()


def print_logo() -> None:
    logo = r"""
███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
█████╗  ██║   ██║██████╔╝██║  ███╗█████╗
██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
"""

    text = Text(logo)
    text.append("\nPython Project Generator", style="bright_black")

    console.print()
    console.print(
        Panel.fit(
            text,
            border_style="bright_black",
            padding=(1, 2),
        )
    )
    console.print()


def print_info(message: str) -> None:
    console.print(f"[cyan]{message}[/cyan]")


def print_success(message: str) -> None:
    console.print(f"[green]OK[/green] {message}")


def print_warning(message: str) -> None:
    console.print(f"[yellow]WARNING[/yellow] {message}")


def print_error(message: str) -> None:
    console.print(f"[red]ERROR[/red] {message}")


@contextmanager
def status(message: str) -> Iterator[None]:
    with console.status(f"[bold]{message}[/bold]", spinner="dots"):
        yield

    print_success(message)