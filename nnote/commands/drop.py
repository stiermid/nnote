import click
import shutil
from ..config import Config
from ..notes import resolve_note_path


@click.command()
@click.argument("title", required=False, default=None)
@click.option("-d", "--directory", default=None, help="Subdirectory within notes dir")
def drop(title, directory):
    """Remove a note or a directory."""
    config = Config.load()

    if config.notes_dir is None:
        raise click.ClickException(
            "Notes directory not configured. Run `nnote init` first."
        )

    if title is None and directory is None:
        raise click.UsageError("Provide a note title, a directory (-d), or both.")

    if title:
        note_path = resolve_note_path(config, title, directory)
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
