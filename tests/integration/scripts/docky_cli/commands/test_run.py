import shutil
from unittest.mock import patch

import pytest

from scripts.cly.utils import run_command
from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import run
from tests import InputOptions, cli_for_tests, override_dependencies


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_run_help(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, ["run", *option])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert all(
        word in output
        for word in [
            "Execute",
            "service",
            "Container",
            "default",
            "command",
            "or",
            "run",
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
def test_run(capfd: pytest.CaptureFixture[str]) -> None:
    @override_dependencies(run)
    def execute(common_command: InputOptions) -> int:
        with patch.object(run, "SERVICE_NAME", "for-tests"):
            exit_code = cli_for_tests(CLI, ["run"])
            run_command(
                [
                    *common_command,
                    "down",
                    "--volumes",
                    "--rmi",
                    "'all'",
                ]
            )
        return exit_code

    exit_code = execute()  # pylint: disable=no-value-for-parameter
    output, error = capfd.readouterr()
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
def test_run_with_command(capfd: pytest.CaptureFixture[str]) -> None:
    @override_dependencies(run)
    def execute(common_command: InputOptions) -> int:
        with patch.object(run, "SERVICE_NAME", "for-tests"):
            exit_code = cli_for_tests(CLI, ["run", "echo", "hello", "there"])
            run_command(
                [
                    *common_command,
                    "down",
                    "--volumes",
                    "--rmi",
                    "'all'",
                ]
            )
        return exit_code

    exit_code = execute()  # pylint: disable=no-value-for-parameter
    output, error = capfd.readouterr()
    assert exit_code == 0
    assert all(
        word in error for word in ["Creating", "network", "Building", "Image"]
    )
    assert all(
        word in output
        for word in ["Running", "command", "in", "Container", "hello", "there"]
    )
