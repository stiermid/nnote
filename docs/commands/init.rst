nnote init
==========

.. code-block:: text

   nnote init

Initialize nnote configuration. Prompts for a notes directory (default:
``~/nnotes``), a default editor, and an optional default backup directory, then
writes ``~/.config/nnote/config.yaml``.

The notes directory is created if it doesn't exist. If ``$EDITOR`` is set in
your environment, it is used as the editor default. The backup directory prompt
can be left blank to skip setting it. Re-running ``init`` re-prompts with your
current values as defaults, so it's safe to use for updating any setting.

.. code-block:: bash

   nnote init
