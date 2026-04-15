import click
from ..config import Config
from ..notes import resolve_note_path, open_in_editor


@click.command()
@click.argument("title", required=False, default=None)
@click.option("-d", "--directory", default=None, help="Subdirectory within notes dir")
def new(title, directory):
    """Create a new note and open it in the configured editor."""
    config = Config.load()
    if title is None:
        if directory is None:
            raise click.UsageError("Provide a title or a directory with -d.")
        if config.notes_dir is None:
            raise click.ClickException("Notes directory not configured. Run `nnote init` first.")
        (config.notes_dir / directory).mkdir(parents=True, exist_ok=True)
        return
    note_path = resolve_note_path(config, title, directory)
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.touch()
    open_in_editor(config, note_path)
