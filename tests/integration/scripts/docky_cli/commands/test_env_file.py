from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import env_file
from tests import DATA_FOLDER, InputOptions, cli_for_tests


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_env_help(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, ["env", *option])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert all(
        word in output
        for word in [
            "Create",
            ".env",
            "file",
            "in",
            "project's",
            "root,",
            "if",
            "it",
            "does",
            "not",
            "already",
            "exists.",
        ]
    )


def test_env_create_env_file(capsys: pytest.CaptureFixture[str]) -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", "for-tests"):
                exit_code = cli_for_tests(CLI, ["env"])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert ".env file created" in output


def test_env_env_file_already_exists(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with patch.object(env_file, "ENV_FILE", DATA_FOLDER / "test_env.env"):
        exit_code = cli_for_tests(CLI, ["env"])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert not output


def test_env_create_env_file_no_service_name_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", ""):
                exit_code = cli_for_tests(CLI, ["env"])
    output, error = capsys.readouterr()
    assert exit_code == 1
    assert not error
    assert "SERVICE_NAME is not set" in output


def test_env_create_env_file_service_name_uppercase_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", "FOR-TESTS"):
                exit_code = cli_for_tests(CLI, ["env"])
    output, error = capsys.readouterr()
    assert exit_code == 1
    assert not error
    assert "SERVICE_NAME is not lowercase" in output


@pytest.mark.parametrize("option", [["-s"], ["--show"]])
def test_env_show_env_file_variables(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", "for-tests"):
                exit_code = cli_for_tests(CLI, ["env", *option])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert "GROUP_ID" in output
    assert "USER_ID" in output
    assert "USER_NAME" in output
    assert "SERVICE_NAME" in output
    assert "WORK_DIR" in output
