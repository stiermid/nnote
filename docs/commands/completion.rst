completion
==========

.. code-block:: none

   nnote completion SHELL

Print the shell activation line needed to enable tab completion for ``nnote``.

``SHELL`` must be one of ``bash``, ``zsh``, or ``fish``.

Once the line is added to your shell config and the shell is restarted (or the
config is sourced), pressing :kbd:`Tab` after a command will complete note
titles and subdirectory names dynamically.

Examples
--------

**bash** — add to ``~/.bashrc``:

.. code-block:: bash

   eval "$(_NNOTE_COMPLETE=bash_source nnote)"

**zsh** — add to ``~/.zshrc``:

.. code-block:: zsh

   eval "$(_NNOTE_COMPLETE=zsh_source nnote)"

**fish** — add to ``~/.config/fish/config.fish``:

.. code-block:: fish

   eval (env _NNOTE_COMPLETE=fish_source nnote)

What gets completed
-------------------

- **Note titles** — for ``edit``, ``view``, ``drop``, and ``move`` (both
  source and destination title arguments). Completion respects the ``-d``
  option: if ``-d mydir`` is already on the command line, only notes inside
  ``mydir/`` are suggested.
- **Subdirectory names** — for the ``-d`` / ``--directory`` option on all
  commands, and ``--dest-dir`` on ``move``.
