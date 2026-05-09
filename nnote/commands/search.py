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
@click.option(
    "--title-only",
    is_flag=True,
    default=False,
    help="Only show notes matched by title",
)
@click.option(
    "--content-only",
    is_flag=True,
    default=False,
    help="Only show notes matched by content",
)
def search(query, directory, limit, title_only, content_only):
    """Search notes by title and content."""
    if title_only and content_only:
        raise click.UsageError(
            "--title-only and --content-only are mutually exclusive."
        )

    config = Config.load()

    if config.notes_dir is None:
        raise click.ClickException(
            "Notes directory not configured. Run `nnote init` first."
        )

    root = config.notes_dir / directory if directory else config.notes_dir

    if not root.exists():
        raise click.ClickException(f"Directory not found: {root}")

    results = search_notes(root, query)
    if title_only:
        results = [r for r in results if r.title_match]
    elif content_only:
        results = [r for r in results if r.matching_lines]
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
