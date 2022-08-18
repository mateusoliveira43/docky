import pytest

from scripts.docky_cli.__main__ import CLI
from tests import InputOptions, cli_for_tests


@pytest.mark.parametrize("option", [[], ["-h"], ["--help"]])
def test_docky_help(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, option)
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert all(command in output for command in CLI.commands)


@pytest.mark.parametrize("option", [["-v"], ["--version"]])
def test_docky_version(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, option)
    output, error = capsys.readouterr()
    assert exit_code == 0
    assert not error
    assert all(word in output for word in ["Docky", "version"])


@pytest.mark.parametrize("option", [["-n"], ["--wrong"]])
def test_docky_options_without_command(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, option)
    output, error = capsys.readouterr()
    assert exit_code == 2
    assert not output
    assert "arguments are required: command" in error


@pytest.mark.parametrize("option", [["not"], ["cook"]])
def test_docky_wrong_commands(
    option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, option)
    output, error = capsys.readouterr()
    assert exit_code == 2
    assert not output
    assert "argument command: invalid choice" in error


@pytest.mark.parametrize("option", [["-n"], ["--wrong"]])
@pytest.mark.parametrize("command", CLI.commands)
def test_docky_commands_with_wrong_options(
    command: str, option: InputOptions, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = cli_for_tests(CLI, [*option, command])
    output, error = capsys.readouterr()
    assert exit_code == 2
    assert not output
    assert "unrecognized arguments" in error
