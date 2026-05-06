Shell completion
================

``nnote`` supports tab completion for note titles and subdirectory names in
**bash**, **zsh**, and **fish**.

Installing
----------

Run once to append the activation line to your shell config automatically:

.. code-block:: bash

   nnote --install-completion

To inspect the line before installing, use:

.. code-block:: bash

   nnote --show-completion

Then restart your shell (or ``source`` the config file) for the change to
take effect.

What gets completed
-------------------

- **Note titles** — for ``edit``, ``view``, ``drop``, and ``move``.
  Both bare filenames (``note``) and path-style input (``dir1/note``) are
  supported; typing ``dir1/`` and pressing :kbd:`Tab` lists notes inside
  that subdirectory.
- **Subdirectory names** — for the ``-d`` / ``--directory`` option on all
  commands, and ``--dest-dir`` on ``move``.
