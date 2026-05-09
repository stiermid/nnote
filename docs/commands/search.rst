nnote search
============

.. code-block:: text

   nnote search <query> [-d <dir>] [-n <limit>]

Search notes by title and content. Results are ranked by relevance: exact
title matches score highest, followed by prefix/substring/fuzzy title matches,
then content hits. Matched terms are highlighted in the output.

Use ``-n`` / ``--limit`` to cap the number of results shown.

.. code-block:: bash

   nnote search meeting
   nnote search budget -d work
   nnote search todo -n 5

::

   work/meeting [title]
     3: discussed the project budget
     7: next meeting on friday
