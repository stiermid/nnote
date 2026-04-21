Configuration
=============

``~/.config/nnote/config.yaml``

.. code-block:: yaml

   notes_dir: /home/user/nnotes
   editor: nvim
   backup_dir: /home/user/backups

The ``editor`` field can be any terminal editor command (``vim``, ``nano``,
``hx``, etc.). If omitted, ``$EDITOR`` is used.

The ``backup_dir`` field sets the default output directory for ``nnote backup``.
When set, backups are written there instead of the current directory. It can be
set during ``nnote init`` or added manually to the config file.
