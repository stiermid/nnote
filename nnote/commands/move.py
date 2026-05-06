import click
from ..config import Config
from ..notes import resolve_note_path
from ..completions import complete_note_titles, complete_directories


@click.command()
@click.argument("title", shell_complete=complete_note_titles)
@click.argument(
    "dest_title", required=False, default=None, shell_complete=complete_note_titles
)
@click.option(
    "-d",
    "--directory",
    default=None,
    help="Source subdirectory",
    shell_complete=complete_directories,
)
@click.option(
    "--dest-dir",
    default=None,
    help="Destination subdirectory",
    shell_complete=complete_directories,
)
def move(title, dest_title, directory, dest_dir):
    """Move or rename a note."""
    config = Config.load()

    if config.notes_dir is None:
        raise click.ClickException(
            "Notes directory not configured. Run `nnote init` first."
        )

    if dest_title is None and dest_dir is None:
        raise click.UsageError(
            "Provide a new title and/or a destination directory (--dest-dir)."
        )

    src = resolve_note_path(config, title, directory)
    if not src.exists():
        raise click.ClickException(f"Note not found: {src}")

    new_title = dest_title if dest_title is not None else title
    dst = resolve_note_path(
        config, new_title, dest_dir if dest_dir is not None else directory
    )

    if dst == src:
        raise click.ClickException("Source and destination are the same.")

    if dst.exists():
        raise click.ClickException(f"A note already exists at: {dst}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dst)
    click.echo(f"Moved: {src.name} -> {dst.relative_to(config.notes_dir)}")
