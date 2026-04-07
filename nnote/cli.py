import click
from .__version__ import VERSION
from .commands.init import init
from .commands.new import new
from .commands.view import view
from .commands.edit import edit
from .commands.list import list_notes
from .commands.drop import drop
from .commands.search import search
from .commands.move import move


@click.group()
@click.version_option(version=VERSION, prog_name="nnote")
def cli():
    """nnote - a note-taking CLI."""
    pass


cli.add_command(init)
cli.add_command(new)
cli.add_command(view)
cli.add_command(edit)
cli.add_command(list_notes)
cli.add_command(drop)
cli.add_command(search)
cli.add_command(move)
