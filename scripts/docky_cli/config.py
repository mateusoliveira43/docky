"""Config file for Docky."""

import shutil
from pathlib import Path

from cly.colors import color_text

USER_NAME: str = "develop"
SERVICE_NAME: str = "docky"
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
COMPOSE_FILE: Path = PROJECT_ROOT / "docker/docker-compose.yaml"

COMMON_COMMAND = [
    "docker-compose",
    "--file",
    COMPOSE_FILE.as_posix(),
    "--project-directory",
    PROJECT_ROOT.as_posix(),  # pylint: disable=no-member
]


def alert_error(message: str) -> None:
    """
    Alert error to user.

    Parameters
    ----------
    message : str
        Error message.

    Raises
    ------
    SystemExit
        Exit with error code 1.

    """
    print(color_text(f"ERROR: {message}", "red"))
    raise SystemExit(1)


def check_docker_and_compose() -> None:
    """
    Check if Docker and Docker Compose are installed and in the path.

    Check if Docker ('docker' executable) is installed and in the path. If not,
    exits with error and message.
    Check if Docker Compose ('docker-compose' executable) is installed and in
    the path. If not, exits with error and message.

    """
    if shutil.which("docker") is None:
        alert_error("Docker is not installed or in the path.")
    if shutil.which("docker-compose") is None:
        alert_error("Docker Compose is not installed or in the path.")