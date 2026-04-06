import click
from ..config import Config
from ..notes import resolve_note_path, open_in_editor


@click.command()
@click.argument("title")
@click.option("-d", "--directory", default=None, help="Subdirectory within notes dir")
def edit(title, directory):
    """Open an existing note in the configured editor."""
    config = Config.load()
    note_path = resolve_note_path(config, title, directory)

    if not note_path.exists():
        raise click.ClickException(f"Note not found: {note_path}")

    open_in_editor(config, note_path)
