import click
from ..config import Config
from ..notes import resolve_note_path


@click.command()
@click.argument("title")
@click.option("-d", "--directory", default=None, help="Subdirectory within notes dir")
def view(title, directory):
    """Print the contents of a note."""
    config = Config.load()
    note_path = resolve_note_path(config, title, directory)

    if not note_path.exists():
        raise click.ClickException(f"Note not found: {note_path}")

    click.echo(note_path.read_text(encoding="utf-8"), nl=False)
