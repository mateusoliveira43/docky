Changelog
=========

1.1.1
-----

In this version:

- Better help messages for commands.

1.0.1
-----

In this version:

- **up command**: Start all services (of compose file) command.
- Script to install/update **Docky** in your project.

1.0.0
-----

**First version of Docky!**

In this version:

- ``.env`` file management command.
- Run a command in pre defined service (of compose file) command.
- List all Docker objects (Containers, Networks, Images and Volumes) command.
- Lint pre defined Dockerfile command.
- Security vulnerability scan for pre defined service Image command.
- Remove all Docker objects (of compose file) command.

For next versions, I want to:

- Add up command for the CLI.
- Add a configuration file outside the code (currently it is in ``docky_cli/config.py``).
- Improve command's help messages.
- Add init command to CLI (to create folders and files for Docker).
- Read Docker's folder and files, so the CLI creates the Dockerfiles, compose
  files and services options to user.
