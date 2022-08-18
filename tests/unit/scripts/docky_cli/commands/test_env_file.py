from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from scripts.docky_cli.commands import env_file
from scripts.docky_cli.commands.env_file import create_env_file, read_env_file
from tests import data


def test_create_env_file(capsys: pytest.CaptureFixture[str]) -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", "for-tests"):
                create_env_file()
    output, error = capsys.readouterr()
    assert not error
    assert ".env file created" in output


def test_create_env_file_file_already_exists(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with patch.object(
        env_file, "ENV_FILE", Path(data.__file__).parent / "test_env.env"
    ):
        create_env_file()
    output, error = capsys.readouterr()
    assert not error
    assert not output


def test_create_env_file_no_service_name_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", ""):
                with pytest.raises(SystemExit) as sys_exit:
                    create_env_file()
    output, error = capsys.readouterr()
    assert sys_exit.value.code == 1
    assert not error
    assert "SERVICE_NAME is not set" in output


def test_create_env_file_service_name_uppercase_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with TemporaryDirectory() as temporary_directory:
        with patch.object(
            env_file, "ENV_FILE", Path(temporary_directory) / ".env"
        ):
            with patch.object(env_file, "SERVICE_NAME", "FOR-TESTS"):
                with pytest.raises(SystemExit) as sys_exit:
                    create_env_file()
    output, error = capsys.readouterr()
    assert sys_exit.value.code == 1
    assert not error
    assert "SERVICE_NAME is not lowercase" in output


def test_read_env_file() -> None:
    with patch.object(
        env_file, "ENV_FILE", Path(data.__file__).parent / "test_env.env"
    ):
        variables = read_env_file()
    assert variables["Obi-Wan"] == "Kenobi"
    assert variables["Anakin"] == "Skywalker"
    assert variables["Qui-Gon"] == "Jinn"
