import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import pytest

from scripts.cly.utils import run_command
from scripts.docky_cli.__main__ import CLI
from scripts.docky_cli.commands import run
from tests import DATA_FOLDER, InputOptions, cli_for_tests


@pytest.mark.parametrize("option", [["-h"], ["--help"]])
def test_run_help(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, ["run", *option])
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert all(
        word in output
        for word in [
            "Enter",
            "project's",
            "Container",
            "shell",
            "or",
            "run",
            "command",
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
def test_run(capfd: pytest.CaptureFixture[str]) -> None:
    with TemporaryDirectory() as temporary_directory:
        temporary_path = Path(temporary_directory)
        (temporary_path / "docker").mkdir(parents=True, exist_ok=True)
        dockerfile = temporary_path / "docker/Dockerfile"
        compose_file = temporary_path / "docker/docker-compose.yaml"
        shutil.copyfile(DATA_FOLDER / "docker/Dockerfile", dockerfile)
        shutil.copyfile(
            DATA_FOLDER / "docker/docker-compose.yaml",
            compose_file,
        )
        common_command = [
            "docker-compose",
            "--file",
            compose_file.as_posix(),
            "--project-directory",
            temporary_path.as_posix(),
        ]
        with patch.object(run, "COMMON_COMMAND", common_command):
            with patch.object(run, "create_env_file", Mock):
                with patch.object(run, "SERVICE_NAME", "for-tests"):
                    exit_code = cli_for_tests(CLI, ["run"])
                    run_command(
                        [
                            *common_command,
                            "down",
                            "--volumes",
                            "--rmi",
                            "'all'",
                        ]
                    )
    output, error = capfd.readouterr()
    assert exit_code == 0
    assert all(
        word in error for word in ["Creating", "network", "Building", "Image"]
    )
    assert all(
        word in output
        for word in ["Running", "command", "in", "Container", "for", "tests"]
    )


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="docker is not available",
)
@pytest.mark.skipif(
    shutil.which("docker-compose") is None,
    reason="docker-compose is not available",
)
def test_run_with_command(capfd: pytest.CaptureFixture[str]) -> None:
    with TemporaryDirectory() as temporary_directory:
        temporary_path = Path(temporary_directory)
        (temporary_path / "docker").mkdir(parents=True, exist_ok=True)
        dockerfile = temporary_path / "docker/Dockerfile"
        compose_file = temporary_path / "docker/docker-compose.yaml"
        shutil.copyfile(DATA_FOLDER / "docker/Dockerfile", dockerfile)
        shutil.copyfile(
            DATA_FOLDER / "docker/docker-compose.yaml",
            compose_file,
        )
        common_command = [
            "docker-compose",
            "--file",
            compose_file.as_posix(),
            "--project-directory",
            temporary_path.as_posix(),
        ]
        with patch.object(run, "COMMON_COMMAND", common_command):
            with patch.object(run, "create_env_file", Mock):
                with patch.object(run, "SERVICE_NAME", "for-tests"):
                    exit_code = cli_for_tests(
                        CLI, ["run", "echo", "hello", "there"]
                    )
                    run_command(
                        [
                            *common_command,
                            "down",
                            "--volumes",
                            "--rmi",
                            "'all'",
                        ]
                    )
    output, error = capfd.readouterr()
    assert exit_code == 0
    assert all(
        word in error for word in ["Creating", "network", "Building", "Image"]
    )
    assert all(
        word in output
        for word in ["Running", "command", "in", "Container", "hello", "there"]
    )
