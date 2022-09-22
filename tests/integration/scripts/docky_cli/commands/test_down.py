import shutil
from typing import Tuple

import pytest

from scripts.cly.testing import run_cli
from scripts.cly.utils import get_returncode
from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import down
from tests import InputOptions, override_dependencies


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_down_help(option: InputOptions) -> None:
    exit_code, output, error = run_cli(CLI, ["down", *option])
    assert exit_code == 0
    assert not error
    assert all(
        word in output
        for word in [
            "Remove",
            "all",
            "Containers,",
            "Networks,",
            "Images",
            "and",
            "Volumes",
            "in",
            "compose",
            "file",
        ]
    )


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="docker is not available",
)
@pytest.mark.skipif(
    shutil.which("docker-compose") is None,
    reason="docker-compose is not available",
)
def test_down() -> None:
    @override_dependencies(down)
    def execute(common_command: InputOptions) -> Tuple[int, str, str]:
        assert not get_returncode([*common_command, "run", "for-tests"])
        return run_cli(CLI, ["down"])  # type: ignore

    (
        exit_code,
        output,
        error,
    ) = execute()  # pylint: disable=no-value-for-parameter
    assert exit_code == 0
    assert not all(word in error for word in ["found"])
    assert all(
        word in output
        for word in ["Removing", "Containers", "Networks", "Images", "Volumes"]
    )


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="docker is not available",
)
@pytest.mark.skipif(
    shutil.which("docker-compose") is None,
    reason="docker-compose is not available",
)
def test_down_without_targets() -> None:
    @override_dependencies(down)
    def execute() -> Tuple[int, str, str]:
        return run_cli(CLI, ["down"])  # type: ignore

    exit_code, output, error = execute()
    assert exit_code == 0
    assert all(word in error for word in ["not", "found"])
    assert all(
        word in output
        for word in ["Removing", "Containers", "Networks", "Images", "Volumes"]
    )
