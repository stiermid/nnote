nnote view
==========

.. code-block:: text

   nnote view <title> [-d <dir>] [--pager]

Print the contents of a note to stdout.

Use ``--pager`` to pipe the output through a pager (``$PAGER``, falling back
to ``less``). Useful for long notes.

.. code-block:: bash

   nnote view todo
   nnote view standup -d work
   nnote view meeting-notes --pager
