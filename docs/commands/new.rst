nnote new
=========

.. code-block:: text

   nnote new [<title>] [-d <dir>]

Create a new note and open it in the configured editor. Use ``-d`` to place
the note inside a subdirectory of your notes directory (created automatically
if it doesn't exist).

Omit the title and provide only ``-d`` to create a directory without opening
an editor.

.. code-block:: bash

   nnote new todo
   nnote new standup -d work
   nnote new -d archive
