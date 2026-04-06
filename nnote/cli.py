import click
import difflib
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from .__version__ import VERSION
from .config import Config, DEFAULT_NOTES_DIR


@click.group()
@click.version_option(version=VERSION, prog_name="nnote")
def cli():
    """nnote - a note-taking CLI."""
    pass


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _resolve_note_path(config: Config, title: str, directory: str | None) -> Path:
    if config.notes_dir is None:
        raise click.ClickException("Notes directory not configured. Run `nnote init` first.")
    base = config.notes_dir / directory if directory else config.notes_dir
    return base / title


def _open_in_editor(config: Config, path: Path) -> None:
    if config.editor is None:
        raise click.ClickException(
            "No editor configured. Set 'editor' in config or the $EDITOR environment variable."
        )
    subprocess.call([config.editor, str(path)])


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

@cli.command()
def init():
    """Initialize nnote configuration."""
    config = Config.load()

    raw = click.prompt(
        "Notes directory",
        default=str(config.notes_dir or DEFAULT_NOTES_DIR),
    )
    notes_dir = Path(raw).expanduser()
    notes_dir.mkdir(parents=True, exist_ok=True)

    editor = click.prompt(
        "Default editor",
        default=config.editor or "vi",
    )

    config.set("notes_dir", value=str(notes_dir))
    config.set("editor", value=editor)
    config.save()

    click.echo(f"Config saved to {config._path}")
    click.echo(f"Notes directory: {notes_dir}")
    click.echo(f"Editor: {editor}")


@cli.command()
@click.argument("title")
@click.option("-d", "--directory", default=None, help="Subdirectory within notes dir")
def new(title, directory):
    """Create a new note and open it in the configured editor."""
    config = Config.load()
    note_path = _resolve_note_path(config, title, directory)
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.touch()
    _open_in_editor(config, note_path)


@cli.command()
@click.argument("title")
@click.option("-d", "--directory", default=None, help="Subdirectory within notes dir")
def view(title, directory):
    """Print the contents of a note."""
    config = Config.load()
    note_path = _resolve_note_path(config, title, directory)

    if not note_path.exists():
        raise click.ClickException(f"Note not found: {note_path}")

    click.echo(note_path.read_text(encoding="utf-8"), nl=False)


@cli.command()
@click.argument("title")
@click.option("-d", "--directory", default=None, help="Subdirectory within notes dir")
def edit(title, directory):
    """Open an existing note in the configured editor."""
    config = Config.load()
    note_path = _resolve_note_path(config, title, directory)

    if not note_path.exists():
        raise click.ClickException(f"Note not found: {note_path}")

    _open_in_editor(config, note_path)


def _print_tree(root: Path, prefix: str = "") -> int:
    entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name))
    count = 0
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        if entry.is_dir():
            click.echo(f"{prefix}{connector}{entry.name}/")
            extension = "    " if i == len(entries) - 1 else "│   "
            count += _print_tree(entry, prefix + extension)
        else:
            click.echo(f"{prefix}{connector}{entry.name}")
            count += 1
    return count


@cli.command(name="list")
@click.option("-d", "--directory", default=None, help="Subdirectory to list")
def list_notes(directory):
    """List notes and directories."""
    config = Config.load()

    if config.notes_dir is None:
        raise click.ClickException("Notes directory not configured. Run `nnote init` first.")

    root = config.notes_dir / directory if directory else config.notes_dir

    if not root.exists():
        raise click.ClickException(f"Directory not found: {root}")

    click.echo(str(root))
    count = _print_tree(root)

    if count == 0:
        click.echo("  (no notes)")


@cli.command()
@click.argument("title", required=False, default=None)
@click.option("-d", "--directory", default=None, help="Subdirectory within notes dir")
def drop(title, directory):
    """Remove a note or a directory."""
    config = Config.load()

    if config.notes_dir is None:
        raise click.ClickException("Notes directory not configured. Run `nnote init` first.")

    if title is None and directory is None:
        raise click.UsageError("Provide a note title, a directory (-d), or both.")

    if title:
        note_path = _resolve_note_path(config, title, directory)
        if not note_path.exists():
            raise click.ClickException(f"Note not found: {note_path}")
        note_path.unlink()
        click.echo(f"Removed: {note_path.name}")
    else:
        dir_path = config.notes_dir / directory
        if not dir_path.exists():
            raise click.ClickException(f"Directory not found: {dir_path}")

        contents = list(dir_path.iterdir())
        if contents:
            click.confirm(
                f"'{directory}' contains {len(contents)} item(s). Remove anyway?",
                abort=True,
            )

        shutil.rmtree(dir_path)
        click.echo(f"Removed directory: {directory}")


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

_TITLE_EXACT   = 100
_TITLE_PREFIX  =  70
_TITLE_SUBSTR  =  50
_FUZZY_THRESHOLD = 0.6
_FUZZY_WEIGHT    = 40
_CONTENT_LINE_SCORE = 10
_CONTENT_MAX_LINES  =  3


@dataclass
class _SearchResult:
    rel_path: str
    score: float
    title_match: bool
    matching_lines: list[tuple[int, str]] = field(default_factory=list)


def _score_title(query: str, name: str) -> float:
    q, n = query.lower(), name.lower()
    if q == n:
        return _TITLE_EXACT
    if n.startswith(q):
        return _TITLE_PREFIX
    if q in n:
        return _TITLE_SUBSTR
    ratio = difflib.SequenceMatcher(None, q, n).ratio()
    if ratio >= _FUZZY_THRESHOLD:
        return ratio * _FUZZY_WEIGHT
    return 0.0


def _search_notes(root: Path, query: str) -> list[_SearchResult]:
    results: list[_SearchResult] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        rel = str(path.relative_to(root))
        title_score = _score_title(query, path.name)

        matching_lines: list[tuple[int, str]] = []
        try:
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if query.lower() in line.lower():
                    matching_lines.append((lineno, line.strip()))
        except (UnicodeDecodeError, OSError):
            pass

        content_score = min(len(matching_lines) * _CONTENT_LINE_SCORE, _CONTENT_LINE_SCORE * _CONTENT_MAX_LINES)
        total = title_score + content_score

        if total > 0:
            results.append(_SearchResult(
                rel_path=rel,
                score=total,
                title_match=title_score > 0,
                matching_lines=matching_lines[:_CONTENT_MAX_LINES],
            ))

    results.sort(key=lambda r: r.score, reverse=True)
    return results


def _highlight(text: str, query: str) -> str:
    lower = text.lower()
    q = query.lower()
    out, i = "", 0
    while i < len(text):
        if lower[i:i + len(q)] == q:
            out += click.style(text[i:i + len(q)], bold=True, fg="yellow")
            i += len(q)
        else:
            out += text[i]
            i += 1
    return out


@cli.command()
@click.argument("query")
@click.option("-d", "--directory", default=None, help="Scope search to a subdirectory")
def search(query, directory):
    """Search notes by title and content."""
    config = Config.load()

    if config.notes_dir is None:
        raise click.ClickException("Notes directory not configured. Run `nnote init` first.")

    root = config.notes_dir / directory if directory else config.notes_dir

    if not root.exists():
        raise click.ClickException(f"Directory not found: {root}")

    results = _search_notes(root, query)

    if not results:
        click.echo("No notes found.")
        return

    for result in results:
        label = click.style(result.rel_path, bold=True)
        tag = click.style(" [title]", fg="green") if result.title_match else ""
        click.echo(f"{label}{tag}")
        for lineno, line in result.matching_lines:
            click.echo(f"  {click.style(str(lineno), dim=True)}: {_highlight(line, query)}")
