import shutil
from unittest.mock import Mock, patch

import pytest

from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import list_docker_objects
from tests import InputOptions, cli_for_tests


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_list_help(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, ["ls", *option])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert all(
        word in output
        for word in [
            "List",
            "all",
            "Containers",
            "Networks",
            "Images",
            "Volumes",
        ]
    )


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="docker is not available",
)
@patch("subprocess.run")
def test_list(
    mock_subprocess: Mock, capsys: pytest.CaptureFixture[str]
) -> None:
    with patch.object(list_docker_objects, "create_env_file", Mock):
        exit_code = cli_for_tests(CLI, ["ls"])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert "Listing" in output
    assert "container" in mock_subprocess.call_args_list[0][0][0]
    assert "network" in mock_subprocess.call_args_list[1][0][0]
    assert "image" in mock_subprocess.call_args_list[2][0][0]
    assert "volume" in mock_subprocess.call_args_list[3][0][0]


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="docker is not available",
)
@pytest.mark.parametrize("option", [["-a"], ["--all"]])
@patch("subprocess.run")
def test_list_all(
    mock_subprocess: Mock,
    option: InputOptions,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with patch.object(list_docker_objects, "create_env_file", Mock):
        exit_code = cli_for_tests(CLI, ["ls", *option])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert "Listing" in output
    assert "container" in mock_subprocess.call_args_list[0][0][0]
    assert "network" in mock_subprocess.call_args_list[1][0][0]
    assert "image" in mock_subprocess.call_args_list[2][0][0]
    assert "volume" in mock_subprocess.call_args_list[3][0][0]
