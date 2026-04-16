nnote init
==========

.. code-block:: text

   nnote init

Initialize nnote configuration. Prompts for a notes directory (default:
``~/nnotes``) and a default editor, then writes ``~/.config/nnote/config.yaml``.

The notes directory is created if it doesn't exist. If ``$EDITOR`` is set in
your environment, it is used as the editor default. Re-running ``init``
re-prompts with your current values as defaults, so it's safe to use for
updating either setting.

.. code-block:: bash

   nnote init
