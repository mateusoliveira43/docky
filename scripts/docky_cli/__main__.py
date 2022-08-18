"""Docky CLI."""

from cly import config

from . import __version__
from .commands.env_file import env

CLI_CONFIG = {
    "name": "Docky",
    "description": "Docky: Run Docker commands with Python.",
    "epilog": "Docker\N{whale} + Python\N{snake}",
    "version": __version__,
}

CLI = config.ConfiguredParser(CLI_CONFIG)

env_command = CLI.create_command(env)
env_command.add_argument("-s", "--show", action="store_true")
