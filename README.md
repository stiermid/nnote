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

- [`new`](docs/commands/new.md) — create a note (or a subdirectory)
- [`view`](docs/commands/view.md) — print a note to stdout
- [`edit`](docs/commands/edit.md) — open an existing note in the editor
- [`list`](docs/commands/list.md) — display notes as a tree
- [`drop`](docs/commands/drop.md) — remove a note or directory
- [`move`](docs/commands/move.md) — rename or relocate a note
- [`backup`](docs/commands/backup.md) — export notes to a `.tar.gz` archive
- [`search`](docs/commands/search.md) — search notes by title and content

See the [full documentation](docs/README.md) for details. Config file format is documented in [docs/configuration.md](docs/configuration.md).

## License

This project is licensed under the GNU General Public License v3.0 or later. See [LICENSE](LICENSE) for details.
