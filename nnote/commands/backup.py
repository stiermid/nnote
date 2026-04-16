import tarfile
from datetime import date
from pathlib import Path

import click

from ..config import Config


@click.command()
@click.argument("output_path", required=False, default=None)
@click.option("-d", "--directory", default=None, help="Subdirectory to back up")
@click.option("--include-config", is_flag=True, default=False, help="Include config file in backup")
@click.option("--dry-run", is_flag=True, default=False, help="List files without creating archive")
@click.option("--quiet", is_flag=True, default=False, help="Suppress output")
def backup(output_path, directory, include_config, dry_run, quiet):
    """Back up notes to a tar.gz archive."""
    config = Config.load()

    if config.notes_dir is None:
        raise click.ClickException("Notes directory not configured. Run `nnote init` first.")

    root = config.notes_dir / directory if directory else config.notes_dir

    if not root.exists():
        raise click.ClickException(f"Directory not found: {root}")

    config_path = Path("~/.config/nnote/config.yaml").expanduser()

    if dry_run:
        count = 0
        for path in sorted(root.rglob("*")):
            if path.is_file():
                click.echo(str(path.relative_to(root.parent)))
                count += 1
        if include_config and config_path.exists():
            click.echo("config.yaml")
            count += 1
        click.echo(f"\n{count} file(s) would be backed up.")
        return

    if output_path is None:
        filename = f"nnote-backup-{date.today()}.tar.gz"
        output_path = Path.cwd() / filename
    else:
        output_path = Path(output_path)

    count = 0
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(root, arcname=root.name)
        count = sum(1 for p in root.rglob("*") if p.is_file())
        if include_config and config_path.exists():
            tar.add(config_path, arcname="config.yaml")
            count += 1

    if not quiet:
        click.echo(f"Backed up {count} file(s) to {output_path}")
