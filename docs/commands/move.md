# nnote move

```
nnote move <title> [<dest_title>] [-d <dir>] [--dest-dir <dir>]
```

Move or rename a note. Provide a new title to rename, `--dest-dir` to move to another subdirectory, or both.

```bash
nnote move todo done                        # rename
nnote move standup -d work --dest-dir arch  # move to another subdirectory
nnote move standup meeting -d work          # rename within a subdirectory
```
