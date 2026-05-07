Shell completion
================

``nnote`` supports tab completion for note titles and subdirectory names in
**bash**, **zsh**, and **fish**.

Installing
----------

Run once to write a completion script to the appropriate directory for
your shell:

.. code-block:: bash

   nnote --install-completion

This does **not** modify any shell config file. The script is placed in an
appropriate completion directory for your shell:

- **bash** — ``~/.local/share/bash-completion/completions/nnote``
- **zsh** — the first directory under ``$HOME`` that is already in your ``$fpath``
- **fish** — ``~/.config/fish/completions/nnote.fish``

To inspect the script before installing, use:

.. code-block:: bash

   nnote --show-completion

Restart your shell for the change to take effect.

What gets completed
-------------------

- **Note titles** — for ``edit``, ``view``, ``drop``, and ``move``.
  Both bare filenames (``note``) and path-style input (``dir1/note``) are
  supported; typing ``dir1/`` and pressing :kbd:`Tab` lists notes inside
  that subdirectory.
- **Subdirectory names** — for the ``-d`` / ``--directory`` option on all
  commands, and ``--dest-dir`` on ``move``.
