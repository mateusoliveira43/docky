import shutil
from unittest.mock import patch

import pytest

from scripts.docky_cli.errors import alert_error, check_docker_and_compose


def test_alert_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as sys_exit:
        alert_error("TEST")
    output, error = capsys.readouterr()
    assert sys_exit.value.code == 1
    assert not error
    assert "TEST" in output


def test_check_docker_and_compose(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(shutil, "which", lambda command: command):
        check_docker_and_compose()
    output, error = capsys.readouterr()
    assert not error
    assert not output


def test_check_docker_and_compose_docker_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with patch.object(shutil, "which", lambda command: None):
        with pytest.raises(SystemExit) as sys_exit:
            check_docker_and_compose()
    output, error = capsys.readouterr()
    assert sys_exit.value.code == 1
    assert not error
    assert "Docker" in output


def test_check_docker_and_compose_compose_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with patch.object(
        shutil,
        "which",
        lambda command: command if command == "docker" else None,
    ):
        with pytest.raises(SystemExit) as sys_exit:
            check_docker_and_compose()
    output, error = capsys.readouterr()
    assert sys_exit.value.code == 1
    assert not error
    assert "Compose" in output
