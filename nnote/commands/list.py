import click
from pathlib import Path
from ..config import Config
from ..completions import complete_directories


def _print_tree(root: Path, prefix: str = "") -> int:
    entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name))
    count = 0
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        if entry.is_dir():
            click.echo(f"{prefix}{connector}{entry.name}/")
            extension = "    " if i == len(entries) - 1 else "│   "
            count += _print_tree(entry, prefix + extension)
        else:
            click.echo(f"{prefix}{connector}{entry.name}")
            count += 1
    return count


@click.command(name="list")
@click.option(
    "-d",
    "--directory",
    default=None,
    help="Subdirectory to list",
    shell_complete=complete_directories,
)
def list_notes(directory):
    """List notes and directories."""
    config = Config.load()

    if config.notes_dir is None:
        raise click.ClickException(
            "Notes directory not configured. Run `nnote init` first."
        )

    root = config.notes_dir / directory if directory else config.notes_dir

    if not root.exists():
        raise click.ClickException(f"Directory not found: {root}")

    click.echo(str(root))
    count = _print_tree(root)

    if count == 0:
        click.echo("  (no notes)")
