nnote
=====

A minimal CLI note-taking tool. Notes are plain files stored in a directory of your choice.

Installation
------------

**Arch Linux (AUR)**

.. code-block:: bash

   yay -S nnote

Or with any other AUR helper, or manually via ``makepkg``.

**From source**

.. code-block:: bash

   pip install -e .

Setup
-----

.. code-block:: bash

   nnote init

Prompts for a notes directory (default: ``~/nnotes``) and a default editor.
Config is saved to ``~/.config/nnote/config.yaml``. If ``$EDITOR`` is set in
your environment, it will be used as the editor default.

.. toctree::
   :maxdepth: 1
   :caption: Commands

   commands/init
   commands/new
   commands/view
   commands/edit
   commands/list
   commands/drop
   commands/move
   commands/backup
   commands/search
   commands/completion

.. toctree::
   :maxdepth: 1
   :caption: Reference

   configuration
