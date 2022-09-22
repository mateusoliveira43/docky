import shutil
from typing import Tuple
from unittest.mock import patch

import pytest

from scripts.cly.testing import run_cli
from scripts.cly.utils import get_returncode
from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import run
from tests import InputOptions, override_dependencies


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_run_help(option: InputOptions) -> None:
    exit_code, output, error = run_cli(CLI, ["run", *option])
    assert exit_code == 0
    assert not error
    assert all(
        word in output
        for word in [
            "run",
            "service",
            "Container",
            "default",
            "command",
            "or",
            "custom",
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
def test_run() -> None:
    @override_dependencies(run)
    def execute(common_command: InputOptions) -> Tuple[int, str, str]:
        with patch.object(run, "SERVICE_NAME", "for-tests"):
            exit_code, output, error = run_cli(CLI, ["run"])
            assert not get_returncode(
                [
                    *common_command,
                    "down",
                    "--volumes",
                    "--rmi",
                    "'all'",
                ]
            )
        return exit_code, output, error

    (
        exit_code,
        output,
        error,
    ) = execute()  # pylint: disable=no-value-for-parameter
    assert exit_code == 0
    assert all(
        word in error for word in ["Creating", "network", "Building", "Image"]
    )
    assert all(
        word in output
        for word in ["Running", "command", "in", "Container", "for", "tests"]
    )


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="docker is not available",
)
@pytest.mark.skipif(
    shutil.which("docker-compose") is None,
    reason="docker-compose is not available",
)
def test_run_with_command() -> None:
    @override_dependencies(run)
    def execute(common_command: InputOptions) -> Tuple[int, str, str]:
        with patch.object(run, "SERVICE_NAME", "for-tests"):
            exit_code, output, error = run_cli(
                CLI, ["run", "echo", "hello", "there"]
            )
            assert not get_returncode(
                [
                    *common_command,
                    "down",
                    "--volumes",
                    "--rmi",
                    "'all'",
                ]
            )
        return exit_code, output, error

    (
        exit_code,
        output,
        error,
    ) = execute()  # pylint: disable=no-value-for-parameter
    assert exit_code == 0
    assert all(
        word in error for word in ["Creating", "network", "Building", "Image"]
    )
    assert all(
        word in output
        for word in ["Running", "command", "in", "Container", "hello", "there"]
    )
