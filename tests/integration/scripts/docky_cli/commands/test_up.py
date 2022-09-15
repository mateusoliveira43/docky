import shutil

import pytest

from scripts.cly.utils import run_command
from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import up
from tests import InputOptions, cli_for_tests, override_dependencies


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_up_help(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, ["up", *option])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert all(
        word in output
        for word in [
            "Start",
            "all",
            "services",
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
def test_up(capfd: pytest.CaptureFixture[str]) -> None:
    @override_dependencies(up)
    def execute(common_command: InputOptions) -> int:
        exit_code = cli_for_tests(CLI, ["up"])
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
    output, _ = capfd.readouterr()
    assert exit_code == 0
    assert all(word in output for word in ["Starting", "application"])
