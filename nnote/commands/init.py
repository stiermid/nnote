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

    backup_dir_raw = click.prompt(
        "Default backup directory (leave blank to skip)",
        default=str(config.backup_dir) if config.backup_dir else "",
    )

    config.set("notes_dir", value=str(notes_dir))
    config.set("editor", value=editor)
    if backup_dir_raw:
        backup_dir = Path(backup_dir_raw).expanduser()
        backup_dir.mkdir(parents=True, exist_ok=True)
        config.set("backup_dir", value=str(backup_dir))
    config.save()

    click.echo(f"Config saved to {config._path}")
    click.echo(f"Notes directory: {notes_dir}")
    click.echo(f"Editor: {editor}")
    if backup_dir_raw:
        click.echo(f"Backup directory: {backup_dir}")
