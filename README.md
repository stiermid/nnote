# nnote

A minimal CLI note-taking tool. Notes are plain files stored in a directory of your choice.

## Installation

```bash
pip install -e .
```

## Setup

```bash
nnote init
```

Prompts for a notes directory (default: `~/nnotes`) and a default editor. Config is saved to `~/.config/nnote/config.yaml`. If `$EDITOR` is set in your environment, it will be used as the editor default.

## Commands

### `nnote new <title> [-d <dir>]`

Create a new note and open it in the configured editor. Use `-d` to place the note inside a subdirectory of your notes directory (created automatically if it doesn't exist).

```bash
nnote new todo
nnote new standup -d work
```

### `nnote view <title> [-d <dir>]`

Print the contents of a note to stdout.

```bash
nnote view todo
nnote view standup -d work
```

### `nnote edit <title> [-d <dir>]`

Open an existing note in the configured editor. Errors if the note doesn't exist (use `new` to create it).

```bash
nnote edit todo
```

### `nnote list [-d <dir>]`

Display all notes as a tree. Scope to a subdirectory with `-d`.

```bash
nnote list
nnote list -d work
```

```
/home/user/nnotes
├── work/
│   ├── meeting
│   └── standup
└── todo
```

### `nnote drop [<title>] [-d <dir>]`

Remove a note or a directory. When dropping a directory, prompts for confirmation if it contains files.

```bash
nnote drop todo              # remove a note
nnote drop standup -d work   # remove a note inside a subdirectory
nnote drop -d work           # remove the entire directory
```

### `nnote search <query> [-d <dir>]`

Search notes by title and content. Results are ranked by relevance: exact title matches score highest, followed by prefix/substring/fuzzy title matches, then content hits. Matched terms are highlighted in the output.

```bash
nnote search meeting
nnote search budget -d work
```

```
work/meeting [title]
  3: discussed the project budget
  7: next meeting on friday
```

## Config file

`~/.config/nnote/config.yaml`

```yaml
notes_dir: /home/user/nnotes
editor: nvim
```

The `editor` field can be any terminal editor command (`vim`, `nano`, `hx`, etc.). If omitted, `$EDITOR` is used.
