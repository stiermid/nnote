import click
from ..config import Config
from ..notes import resolve_note_path
from ..completions import complete_note_titles, complete_directories


@click.command()
@click.argument("title", shell_complete=complete_note_titles)
@click.option(
    "-d",
    "--directory",
    default=None,
    help="Subdirectory within notes dir",
    shell_complete=complete_directories,
)
@click.option(
    "--pager",
    is_flag=True,
    default=False,
    help="Pipe output through $PAGER (defaults to less)",
)
def view(title, directory, pager):
    """Print the contents of a note."""
    config = Config.load()
    note_path = resolve_note_path(config, title, directory)

    if not note_path.exists():
        raise click.ClickException(f"Note not found: {note_path}")

    content = note_path.read_text(encoding="utf-8")
    if pager:
        click.echo_via_pager(content)
    else:
        click.echo(content, nl=False)
