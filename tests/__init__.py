import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from typing import Any, Callable, List, Optional
from unittest.mock import Mock, patch

from scripts.cly.config import ConfiguredParser

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = Path(__file__).resolve().parent / "data"
SCRIPTS_FOLDER = PROJECT_ROOT / "scripts"
if SCRIPTS_FOLDER.exists():
    # Since scripts is not a Python package, this is needed
    sys.path.append(SCRIPTS_FOLDER.as_posix())

InputOptions = List[Optional[str]]


def cli_for_tests(cli: ConfiguredParser, sys_mock: InputOptions) -> int:
    """
    Test CLI with passed arguments. Returns the exit code of the operation.

    Parameters
    ----------
    cli : ConfiguredParser
        CLI to test.
    sys_mock : InputOptions
        Arguments to pass to CLI.

    Returns
    -------
    int
        Exit code.
    """
    with patch.object(sys, "argv", ["file_name", *sys_mock]):
        try:
            cli()
            return 0
        except SystemExit as sys_exit:
            return sys_exit.code


def override_dependencies(module: ModuleType) -> Callable[..., Any]:
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
    Callable[..., Any]
        Overridden function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrap(*args: Any, **kwargs: Any) -> Any:
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
