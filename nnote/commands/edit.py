import click
from ..config import Config
from ..notes import resolve_note_path, open_in_editor
from ..completions import complete_note_titles, complete_directories


@click.command()
@click.argument("title", shell_complete=complete_note_titles)
@click.option("-d", "--directory", default=None, help="Subdirectory within notes dir", shell_complete=complete_directories)
def edit(title, directory):
    """Open an existing note in the configured editor."""
    config = Config.load()
    note_path = resolve_note_path(config, title, directory)

    if not note_path.exists():
        raise click.ClickException(f"Note not found: {note_path}")

    open_in_editor(config, note_path)
