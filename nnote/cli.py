import click
import subprocess
from pathlib import Path
from .__version__ import VERSION
from .config import Config, DEFAULT_NOTES_DIR


@click.group()
@click.version_option(version=VERSION, prog_name="nnote")
def cli():
    """nnote - a note-taking CLI."""
    pass


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

    if config.notes_dir is None:
        raise click.ClickException("Notes directory not configured. Run `nnote init` first.")

    if config.editor is None:
        raise click.ClickException(
            "No editor configured. Set 'editor' in config or the $EDITOR environment variable."
        )

    if directory:
        note_path = config.notes_dir / directory / title
        note_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        note_path = config.notes_dir / title

    note_path.touch()
    subprocess.call([config.editor, str(note_path)])
