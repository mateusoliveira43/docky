Welcome to Docky's documentation!
=================================

**Docky** is a Command Line Interface (CLI) tool written in Python (using `CLY?!
<https://github.com/mateusoliveira43/cly>`_) for running Docker and Docker
Compose commands.

Usage
-----

To use **Docky** in your project, in your project's root, run::

   curl -fsSL https://raw.githubusercontent.com/mateusoliveira43/docky/main/install_docky.py | python -

This will copy **Docky** (latest version) files to the ``scripts`` folder of your project.
Then add the project's configuration in ``scripts/docky_cli/config.py`` file.

To install (or update) Docky to a specific version, run::

   curl -fsSL https://raw.githubusercontent.com/mateusoliveira43/docky/main/install_docky.py | python - <version>

You can check **Docky** help by running::

   ./scripts/docky.py

.. image:: cli_help.gif
   :alt: Running Docky help

You can check a **Docky** command help by running::

   ./scripts/docky.py <command> --help

where ``<command>`` is one of the commands presented in the **Commands** section
of **Docky** help.

.. image:: cli_command_help.gif
   :alt: Running a Docky command help

To run your project with Docker for development, run::

   ./scripts/docky.py run

.. image:: cli_run_and_build.gif
   :alt: Connecting to Container's shell for the first time

The command will create ``.env`` file in project's root (if it does not already exists),
Build the service's images (and the images it depends on, if they are not already built),
and then connect to the service's Container shell.

You can both run the commands inside the Container's shell

.. image:: run_inside.gif
   :alt: Running command inside Container's shell

or run each command individually, by running::

   ./scripts/docky.py run <command>

where ``<command>`` can be a command and it's arguments.

.. image:: run_outside.gif
   :alt: Running command outside Container's shell

You can add **Docky** to the path, and call it with ``docky`` instead of
``./scripts/docky.py`` by adding **Docky** to ``pyproject.toml``::

   [tool.poetry.scripts]
   docky = "scripts.docky_cli.__main__:CLI"


and running::

   pip install -e ./


.. toctree::
   :maxdepth: 2
   :hidden:

   changelog.rst
   modules/modules.rst
