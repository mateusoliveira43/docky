import shutil
from typing import Tuple

import pytest

from scripts.cly.testing import run_cli
from scripts.cly.utils import get_returncode
from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import up
from tests import InputOptions, override_dependencies


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_up_help(option: InputOptions) -> None:
    exit_code, output, error = run_cli(CLI, ["up", *option])
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
def test_up() -> None:
    @override_dependencies(up)
    def execute(common_command: InputOptions) -> Tuple[int, str, str]:
        exit_code, output, error = run_cli(CLI, ["up"])
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
        _,
    ) = execute()  # pylint: disable=no-value-for-parameter
    assert exit_code == 0
    assert all(word in output for word in ["Starting", "application"])
