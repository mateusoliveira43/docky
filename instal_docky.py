#!/usr/bin/env python3
"""
Install Docky CLI to project.

Install/update Docky latest version or pass version to script (in the format
major.minor.patch), to install/update to specific version.

"""

import shutil
import subprocess  # nosec
import sys
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parent
DOCKY: str = "git@github.com:mateusoliveira43/docky.git"


def get_docky() -> str:
    """
    Get Docky's source code.

    Returns
    -------
    str
        Command to clone Docky's Git repository.

    """
    try:
        return f"git clone --branch {sys.argv[1]} {DOCKY}"
    except IndexError:
        return f"git clone {DOCKY}"


subprocess.run(get_docky(), shell=True, check=True, encoding="utf-8")  # nosec
shutil.copytree(PROJECT_ROOT / "docky/scripts", PROJECT_ROOT / "scripts")
shutil.rmtree(PROJECT_ROOT / "docky")
