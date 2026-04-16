# nnote drop

```
nnote drop [<title>] [-d <dir>]
```

Remove a note or a directory. When dropping a directory, prompts for confirmation if it contains files.

```bash
nnote drop todo              # remove a note
nnote drop standup -d work   # remove a note inside a subdirectory
nnote drop -d work           # remove the entire directory
```
