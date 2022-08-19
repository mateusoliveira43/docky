import sys
from pathlib import Path
from typing import List, Optional
from unittest.mock import patch

from scripts.cly.config import ConfiguredParser

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = Path(__file__).resolve().parent / "data"
SCRIPTS_FOLDER = PROJECT_ROOT / "scripts"
if SCRIPTS_FOLDER.exists():
    sys.path.append(SCRIPTS_FOLDER.as_posix())

InputOptions = List[Optional[str]]


def cli_for_tests(cli: ConfiguredParser, sys_mock: InputOptions) -> int:
    with patch.object(sys, "argv", ["file_name", *sys_mock]):
        try:
            cli()
            return 0
        except SystemExit as sys_exit:
            return sys_exit.code
