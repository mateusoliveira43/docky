import shutil
from unittest.mock import Mock, patch

import pytest

from scripts.docky_cli.__main__ import CLI
from tests import InputOptions, cli_for_tests


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_lint_help(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, ["lint", *option])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert all(
        word in output
        for word in [
            "Lint",
            "Dockerfile",
        ]
    )


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="docker is not available",
)
@patch("subprocess.run")
def test_lint(
    mock_subprocess: Mock, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, ["lint"])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert "Linting" in output
    mock_subprocess.assert_called_once()
    assert "hadolint" in mock_subprocess.call_args[0][0]
