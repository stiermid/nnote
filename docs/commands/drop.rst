nnote drop
==========

.. code-block:: text

   nnote drop [<title> ...] [-d <dir>]

Remove one or more notes or a directory. Multiple titles can be passed in a
single invocation. All titles are validated before anything is deleted — if
any are missing, nothing is removed and the missing names are reported.

When dropping a directory, prompts for confirmation if it contains files.

.. code-block:: bash

   nnote drop todo                       # remove a single note
   nnote drop standup -d work            # remove a note inside a subdirectory
   nnote drop todo shopping errands      # remove multiple notes at once
   nnote drop mon tue wed -d work        # remove multiple notes in a subdirectory
   nnote drop -d work                    # remove the entire directory
