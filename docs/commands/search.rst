nnote search
============

.. code-block:: text

   nnote search <query> [-d <dir>] [-n <limit>] [--title-only | --content-only]

Search notes by title and content. Results are ranked by relevance: exact
title matches score highest, followed by prefix/substring/fuzzy title matches,
then content hits. Matched terms are highlighted in the output.

Use ``-n`` / ``--limit`` to cap the number of results shown.

Use ``--title-only`` to restrict results to notes whose filename matched the
query. Use ``--content-only`` to restrict results to notes with matching lines
in their body. The two flags are mutually exclusive.

.. code-block:: bash

   nnote search meeting
   nnote search budget -d work
   nnote search todo -n 5
   nnote search api --title-only
   nnote search TODO --content-only -n 10

::

   work/meeting [title]
     3: discussed the project budget
     7: next meeting on friday
