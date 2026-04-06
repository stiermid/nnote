# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development setup

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

Run the CLI directly during development:

```bash
python -m nnote <command>
# or after pip install -e .:
nnote <command>
```

## Architecture

The app is split into three layers:

**Core modules** (`nnote/`)
- `config.py` — `Config` class: loads/saves `~/.config/nnote/config.yaml`. Exposes `notes_dir` and `editor` as properties. `editor` falls back to `$EDITOR`.
- `notes.py` — shared helpers used by multiple commands: `resolve_note_path` (builds a `Path` from title + optional subdirectory) and `open_in_editor` (calls `subprocess.call`).
- `search.py` — self-contained search engine: `search_notes(root, query)` scores each note by title match (exact/prefix/substring/fuzzy via `difflib`) and content line hits, returns ranked `SearchResult` list. `highlight` adds terminal colour to matched terms.

**Commands** (`nnote/commands/`)
One file per command. Each file defines a standalone `@click.command()` — no direct reference to `cli`. Commands import from `config`, `notes`, or `search` as needed.

**Entry point** (`nnote/cli.py`)
Defines the `cli` group and registers every command via `cli.add_command()`. This is the only file that knows about all commands.

## Adding a new command

1. Create `nnote/commands/<name>.py` with a `@click.command()` function.
2. Import and register it in `nnote/cli.py` with `cli.add_command(...)`.

## Dependencies

- `click` — CLI framework
- `pyyaml` — config file serialisation
