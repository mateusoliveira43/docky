import pytest

from scripts.docky_cli.config import alert_error


def test_alert_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as sys_exit:
        alert_error("TEST")
    output, error = capsys.readouterr()
    assert sys_exit.value.code == 1
    assert not error
    assert "TEST" in output
