import subprocess
from pathlib import Path
from typing import Sequence

from vylyv_forge.errors import ForgeError


def run_command(command: Sequence[str], cwd: Path, error_message: str) -> None:
    try:
        subprocess.run(
            list(command),
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        raise ForgeError(f"{error_message}. Command not found: {command[0]}")
    except subprocess.CalledProcessError as error:
        command_text = " ".join(command)

        output = ""
        if error.stderr:
            output = error.stderr.strip()
        elif error.stdout:
            output = error.stdout.strip()

        if output:
            raise ForgeError(
                f"{error_message}. Command failed with exit code "
                f"{error.returncode}: {command_text}\n\n{output}"
            )

        raise ForgeError(
            f"{error_message}. Command failed with exit code "
            f"{error.returncode}: {command_text}"
        )