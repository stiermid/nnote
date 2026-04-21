nnote backup
============

.. code-block:: text

   nnote backup [<output_path>] [-d <dir>] [--include-config] [--dry-run] [--quiet]

Back up notes to a ``.tar.gz`` archive. If no output path is given, saves
``nnote-backup-YYYY-MM-DD.tar.gz`` in ``backup_dir`` (if configured) or the
current directory.

- ``-d`` — scope the backup to a subdirectory
- ``--include-config`` — also bundle ``~/.config/nnote/config.yaml`` into the archive
- ``--dry-run`` — list files that would be included without writing anything
- ``--quiet`` — suppress output (useful for scripting)

.. code-block:: bash

   nnote backup                             # nnote-backup-2026-04-16.tar.gz in cwd
   nnote backup ~/backups/notes.tar.gz      # custom output path
   nnote backup -d work                     # only the 'work' subdirectory
   nnote backup --include-config            # include config file
   nnote backup --dry-run                   # preview without creating archive
