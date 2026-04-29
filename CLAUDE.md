# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development setup

```bash
uv sync
```

Run the CLI directly during development:

```bash
uv run nnote <command>
# or
uv run python -m nnote <command>
```

Install extras for tests or docs:

```bash
uv sync --extra dev    # pytest
uv sync --extra docs   # sphinx
```

## Testing

Tests live in `tests/` and run with `pytest`. Run the full suite with:

```bash
uv run pytest
```

or a single file with `uv run pytest tests/test_search.py`.

## Docs

Sphinx sources live in `docs/` (RST). Build the HTML site with:

```bash
uv run sphinx-build -b html docs docs/_build/html
```

The site is also deployed to GitHub Pages.

## Architecture

The app is split into three layers:

**Core modules** (`nnote/`)
- `config.py` — `Config` class: loads/saves `~/.config/nnote/config.yaml`. Exposes `notes_dir` and `editor` as properties. `editor` falls back to `$EDITOR`.
- `notes.py` — shared helpers used by multiple commands: `resolve_note_path` (builds a `Path` from title + optional subdirectory) and `open_in_editor` (calls `subprocess.call`).
- `search.py` — self-contained search engine: `search_notes(root, query)` scores each note by title match (exact/prefix/substring/fuzzy via `difflib`) and content line hits, returns ranked `SearchResult` list. `highlight` adds terminal colour to matched terms.

**Commands** (`nnote/commands/`)
One file per command. Each file defines a standalone `@click.command()` — no direct reference to `cli`. Commands import from `config`, `notes`, or `search` as needed.

**Entry point** (`nnote/cli.py`)
Defines the `cli` group and registers every command via `cli.add_command()`. This is the only file that knows about all commands. The `--version` flag reads `VERSION` from `nnote/__version__.py`.

## Adding a new command

1. Create `nnote/commands/<name>.py` with a `@click.command()` function.
2. Import and register it in `nnote/cli.py` with `cli.add_command(...)`.
3. Add `docs/commands/<name>.rst` and link it from the toctree in `docs/index.rst`.

## Dependencies

- `click` — CLI framework
- `pyyaml` — config file serialisation
