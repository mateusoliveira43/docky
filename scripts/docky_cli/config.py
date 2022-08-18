"""Config file for Docky."""

from pathlib import Path

from cly.colors import color_text

USER_NAME: str = "develop"
SERVICE_NAME: str = "docky"
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
COMPOSE_FILE: Path = PROJECT_ROOT / "docker/docker-compose.yaml"


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
