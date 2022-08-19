import shutil

import pytest

from scripts.cly.utils import run_command
from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import down
from tests import InputOptions, cli_for_tests, override_dependencies


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_down_help(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, ["down", *option])
    output, error = capsys.readouterr()
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
            "of",
            "the",
            "project",
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
def test_down(capfd: pytest.CaptureFixture[str]) -> None:
    @override_dependencies(down)
    def execute(common_command: InputOptions) -> int:
        run_command([*common_command, "run", "for-tests"])
        return cli_for_tests(CLI, ["down"])

    exit_code = execute()  # pylint: disable=no-value-for-parameter
    output, error = capfd.readouterr()
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
def test_down_without_targets(capfd: pytest.CaptureFixture[str]) -> None:
    @override_dependencies(down)
    def execute() -> int:
        return cli_for_tests(CLI, ["down"])

    exit_code = execute()
    output, error = capfd.readouterr()
    assert exit_code == 0
    assert all(word in error for word in ["not", "found"])
    assert all(
        word in output
        for word in ["Removing", "Containers", "Networks", "Images", "Volumes"]
    )
