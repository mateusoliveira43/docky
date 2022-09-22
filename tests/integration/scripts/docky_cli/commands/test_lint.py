import shutil
from unittest.mock import Mock, patch

import pytest

from scripts.cly.testing import run_cli
from scripts.docky_cli.__main__ import CLI
from tests import InputOptions


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_lint_help(option: InputOptions) -> None:
    exit_code, output, error = run_cli(CLI, ["lint", *option])
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
def test_lint(mock_subprocess: Mock) -> None:
    exit_code, output, error = run_cli(CLI, ["lint"])
    assert exit_code == 0
    assert not error
    assert "Linting" in output
    mock_subprocess.assert_called_once()
    assert "hadolint" in mock_subprocess.call_args[0][0]
