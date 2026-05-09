import click
import shutil
from ..config import Config
from ..notes import resolve_note_path
from ..completions import complete_note_titles, complete_directories


@click.command()
@click.argument("titles", nargs=-1, shell_complete=complete_note_titles)
@click.option(
    "-d",
    "--directory",
    default=None,
    help="Subdirectory within notes dir",
    shell_complete=complete_directories,
)
def drop(titles, directory):
    """Remove one or more notes or a directory."""
    config = Config.load()

    if config.notes_dir is None:
        raise click.ClickException(
            "Notes directory not configured. Run `nnote init` first."
        )

    if not titles and directory is None:
        raise click.UsageError("Provide a note title, a directory (-d), or both.")

    if titles:
        paths = [resolve_note_path(config, t, directory) for t in titles]
        missing = [p for p in paths if not p.exists()]
        if missing:
            names = ", ".join(p.name for p in missing)
            raise click.ClickException(f"Note(s) not found: {names}")
        for path in paths:
            path.unlink()
            click.echo(f"Removed: {path.name}")
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
