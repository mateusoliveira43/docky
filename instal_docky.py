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
SOURCE: Path = PROJECT_ROOT / "docky/scripts"


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


def copy_files_to_scripts(folder: Path) -> None:
    """
    Copy files to the project's scripts folder.

    Files with the same name are overwritten.

    Parameters
    ----------
    folder : Path
        Folder or file to be copied.

    """
    for file in folder.glob("*"):
        if file.is_dir():
            copy_files_to_scripts(file)
        else:
            destination = PROJECT_ROOT / "scripts" / file.relative_to(SOURCE)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src=file, dst=destination)


subprocess.run(get_docky(), shell=True, check=True, encoding="utf-8")  # nosec
copy_files_to_scripts(SOURCE)
shutil.rmtree(PROJECT_ROOT / "docky")
