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

## Documentation

Full documentation is published at **https://stiermid.github.io/nnote/**.

Command reference (also browsable in this repo):

- [`new`](docs/commands/new.rst) — create a note (or a subdirectory)
- [`view`](docs/commands/view.rst) — print a note to stdout
- [`edit`](docs/commands/edit.rst) — open an existing note in the editor
- [`list`](docs/commands/list.rst) — display notes as a tree
- [`drop`](docs/commands/drop.rst) — remove a note or directory
- [`move`](docs/commands/move.rst) — rename or relocate a note
- [`backup`](docs/commands/backup.rst) — export notes to a `.tar.gz` archive
- [`search`](docs/commands/search.rst) — search notes by title and content

Config file format: [docs/configuration.rst](docs/configuration.rst).

## License

This project is licensed under the GNU General Public License v3.0 or later. See [LICENSE](LICENSE) for details.
