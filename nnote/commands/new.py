import click
from ..config import Config
from ..notes import resolve_note_path, open_in_editor


@click.command()
@click.argument("title")
@click.option("-d", "--directory", default=None, help="Subdirectory within notes dir")
def new(title, directory):
    """Create a new note and open it in the configured editor."""
    config = Config.load()
    note_path = resolve_note_path(config, title, directory)
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.touch()
    open_in_editor(config, note_path)
