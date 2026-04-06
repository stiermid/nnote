import click
from .__version__ import VERSION
from .config import Config


@click.group()
@click.version_option(version=VERSION, prog_name="nnote")
def cli():
    """nnote - a note-taking CLI."""
    pass


@cli.command()
def init():
    """Initialize nnote configuration."""
    config = Config.load()
    click.echo(f"Initialized nnote config at {config._path}")
