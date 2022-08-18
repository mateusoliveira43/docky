import sys
from runpy import run_path
from unittest.mock import patch

import pytest

from tests import SCRIPTS_FOLDER


def test_run_docky_script(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["file_name"]):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(
                (SCRIPTS_FOLDER / "docky.py").as_posix(), run_name="__main__"
            )
    output, error = capsys.readouterr()
    assert sys_exit.value.code == 0
    assert not error
    assert "Docky" in output
