from argparse import Namespace

from vylyv_forge.generator import create_project


def handle_create_command(args: Namespace) -> None:
    create_project(
        name=args.name,
        template=args.template,
        create_venv=not args.no_venv,
        install_dependencies=not args.no_install,
    )