nnote search
============

.. code-block:: text

   nnote search <query> [-d <dir>]

Search notes by title and content. Results are ranked by relevance: exact
title matches score highest, followed by prefix/substring/fuzzy title matches,
then content hits. Matched terms are highlighted in the output.

.. code-block:: bash

   nnote search meeting
   nnote search budget -d work

::

   work/meeting [title]
     3: discussed the project budget
     7: next meeting on friday
