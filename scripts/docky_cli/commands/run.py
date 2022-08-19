"""Run commands in Docker's Container."""

from typing import List, Optional

from cly.colors import print_flashy
from cly.utils import run_command

from ..config import COMMON_COMMAND, SERVICE_NAME
from ..errors import check_docker_and_compose
from .env_file import create_env_file


def run_command_in_container(command: List[Optional[str]]) -> None:
    """
    Enter project's Container shell or run a command in it.

    If images are not yet built, they are build before running the command.

    If no command is passed, enters the Container's shell (command in compose
    file), otherwise, runs the commands in the Container's shell and exits.

    Parameters
    ----------
    command : List[Optional[str]]
        Command to run instead of entering the Container's shell.

    """
    print_flashy("Running command in Container")
    run_command(
        [
            *COMMON_COMMAND,
            "run",
            "--rm",
            SERVICE_NAME,
            *command,  # type: ignore
        ]
    )


def run(command: List[Optional[str]]) -> None:
    """
    Enter project's Container shell or run a command in it.

    Parameters
    ----------
    command : List[Optional[str]]
        Command to run instead of entering the Container's shell.

    """
    create_env_file()
    check_docker_and_compose()
    run_command_in_container(command)
