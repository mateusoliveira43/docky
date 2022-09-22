from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from scripts.cly.testing import run_cli
from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import env_file
from tests import DATA_FOLDER, InputOptions


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_env_help(option: InputOptions) -> None:
    exit_code, output, error = run_cli(CLI, ["env", *option])
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


def test_env_create_env_file() -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", "for-tests"):
                exit_code, output, error = run_cli(CLI, ["env"])
    assert exit_code == 0
    assert not error
    assert ".env file created" in output


def test_env_env_file_already_exists() -> None:
    with patch.object(env_file, "ENV_FILE", DATA_FOLDER / "test_env.env"):
        exit_code, output, error = run_cli(CLI, ["env"])
    assert exit_code == 0
    assert not error
    assert not output


def test_env_create_env_file_no_service_name_error() -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", ""):
                exit_code, output, error = run_cli(CLI, ["env"])
    assert exit_code == 1
    assert not error
    assert "SERVICE_NAME is not set" in output


def test_env_create_env_file_service_name_uppercase_error() -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", "FOR-TESTS"):
                exit_code, output, error = run_cli(CLI, ["env"])
    assert exit_code == 1
    assert not error
    assert "SERVICE_NAME is not lowercase" in output


@pytest.mark.parametrize("option", [["-s"], ["--show"]])
def test_env_show_env_file_variables(option: InputOptions) -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", "for-tests"):
                exit_code, output, error = run_cli(CLI, ["env", *option])
    assert exit_code == 0
    assert not error
    assert "GROUP_ID" in output
    assert "USER_ID" in output
    assert "USER_NAME" in output
    assert "SERVICE_NAME" in output
    assert "WORK_DIR" in output
