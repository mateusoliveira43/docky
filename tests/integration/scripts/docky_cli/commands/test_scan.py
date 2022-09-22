import shutil
from unittest.mock import Mock, patch

import pytest

from scripts.cly.testing import run_cli
from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import env_file, run, scan
from tests import DATA_FOLDER, InputOptions


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_scan_help(option: InputOptions) -> None:
    exit_code, output, error = run_cli(CLI, ["scan", *option])
    assert exit_code == 0
    assert not error
    assert all(
        word in output
        for word in [
            "Scan",
            "service",
            "Image",
            "security",
        ]
    )


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="docker is not available",
)
def test_scan_without_snyk_token() -> None:
    with patch.object(
        env_file, "ENV_FILE", DATA_FOLDER / "test_without_token.env"
    ):
        exit_code, output, error = run_cli(CLI, ["scan"])
    assert exit_code == 1
    assert not error
    assert "SNYK_TOKEN not set" in output


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="docker is not available",
)
@patch("subprocess.run")
def test_scan_without_image(mock_subprocess: Mock) -> None:
    with patch.object(env_file, "ENV_FILE", DATA_FOLDER / "test_token.env"):
        with patch.object(run, "run", "test"):
            exit_code, output, error = run_cli(CLI, ["scan"])
    assert exit_code == 0
    assert not error
    assert "Scanning" in output
    assert "Image built" in mock_subprocess.call_args_list[1][0][0]
    assert "login" in mock_subprocess.call_args_list[2][0][0]
    assert "scan" in mock_subprocess.call_args_list[3][0][0]
    assert "rm" in mock_subprocess.call_args_list[4][0][0]


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="docker is not available",
)
@patch("subprocess.run")
def test_scan_with_image(mock_subprocess: Mock) -> None:
    mock_subprocess.return_value.stdout = "image"
    with patch.object(env_file, "ENV_FILE", DATA_FOLDER / "test_token.env"):
        with patch.object(scan, "SERVICE_NAME", "image"):
            exit_code, output, error = run_cli(CLI, ["scan"])
    assert exit_code == 0
    assert not error
    assert "Scanning" in output
    assert "login" in mock_subprocess.call_args_list[1][0][0]
    assert "scan" in mock_subprocess.call_args_list[2][0][0]
    assert "rm" in mock_subprocess.call_args_list[3][0][0]
