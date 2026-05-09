import click
from ..config import Config
from ..search import search_notes, highlight
from ..completions import complete_directories


@click.command()
@click.argument("query")
@click.option(
    "-d",
    "--directory",
    default=None,
    help="Scope search to a subdirectory",
    shell_complete=complete_directories,
)
@click.option(
    "-n",
    "--limit",
    default=None,
    type=click.IntRange(min=1),
    help="Maximum number of results to show",
)
def search(query, directory, limit):
    """Search notes by title and content."""
    config = Config.load()

    if config.notes_dir is None:
        raise click.ClickException(
            "Notes directory not configured. Run `nnote init` first."
        )

    root = config.notes_dir / directory if directory else config.notes_dir

    if not root.exists():
        raise click.ClickException(f"Directory not found: {root}")

    results = search_notes(root, query)
    if limit is not None:
        results = results[:limit]

    if not results:
        click.echo("No notes found.")
        return

    for result in results:
        label = click.style(result.rel_path, bold=True)
        tag = click.style(" [title]", fg="green") if result.title_match else ""
        click.echo(f"{label}{tag}")
        for lineno, line in result.matching_lines:
            click.echo(
                f"  {click.style(str(lineno), dim=True)}: {highlight(line, query)}"
            )
