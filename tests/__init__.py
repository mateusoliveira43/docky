import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from typing import Any, Callable, List, Optional, TypeVar
from unittest.mock import Mock, patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = Path(__file__).resolve().parent / "data"
SCRIPTS_FOLDER = PROJECT_ROOT / "scripts"
if SCRIPTS_FOLDER.exists():
    # Since scripts is not a Python package, this is needed
    sys.path.append(SCRIPTS_FOLDER.as_posix())

InputOptions = List[Optional[str]]
ReturnT = TypeVar("ReturnT")


def override_dependencies(
    module: ModuleType,
) -> Callable[[Callable[..., ReturnT]], Callable[..., ReturnT]]:
    """
    Override dependencies for tests.

    Overrides:
    - COMMON_COMMAND to use Dockerfile and compose file in tests/data in a
    temporary directory.
    - create_env_file to not create .env file.

    Parameters
    ----------
    module : ModuleType
        Module where are the variables and functions to be overridden.

    Returns
    -------
    Callable[[Callable[..., ReturnT]], Callable[..., ReturnT]]
        Overridden function.
    """

    def decorator(func: Callable[..., ReturnT]) -> Callable[..., ReturnT]:
        def wrap(*args: Any, **kwargs: Any) -> ReturnT:
            with TemporaryDirectory() as temporary_directory:
                temporary_path = Path(temporary_directory)
                (temporary_path / "docker").mkdir(parents=True, exist_ok=True)
                dockerfile = temporary_path / "docker/Dockerfile"
                compose_file = temporary_path / "docker/docker-compose.yaml"
                shutil.copyfile(DATA_FOLDER / "docker/Dockerfile", dockerfile)
                shutil.copyfile(
                    DATA_FOLDER / "docker/docker-compose.yaml",
                    compose_file,
                )
                common_command = [
                    "docker-compose",
                    "--file",
                    compose_file.as_posix(),
                    "--project-directory",
                    temporary_path.as_posix(),
                ]
                with patch.object(module, "COMMON_COMMAND", common_command):
                    with patch.object(module, "create_env_file", Mock):
                        if "common_command" in func.__code__.co_varnames:
                            return func(
                                common_command=common_command, *args, **kwargs
                            )
                        return func(*args, **kwargs)

        return wrap

    return decorator
