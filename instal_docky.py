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
TAG: str = f"--branch {sys.argv[1]}" if sys.argv[1] else ""
COMMAND: str = f"git clone {TAG} {DOCKY}"

subprocess.run(COMMAND, shell=True, check=True, encoding="utf-8")  # nosec
shutil.copy(PROJECT_ROOT / "docky/scripts", PROJECT_ROOT / "scripts")
shutil.rmtree(PROJECT_ROOT / "docky")
