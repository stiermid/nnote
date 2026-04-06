import click
import shutil
import subprocess
from pathlib import Path
from .__version__ import VERSION
from .config import Config, DEFAULT_NOTES_DIR


@click.group()
@click.version_option(version=VERSION, prog_name="nnote")
def cli():
    """nnote - a note-taking CLI."""
    pass


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
