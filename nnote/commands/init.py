import click
from pathlib import Path
from ..config import Config, DEFAULT_NOTES_DIR


@click.command()
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
