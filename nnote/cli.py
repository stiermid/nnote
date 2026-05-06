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
from .commands.backup import backup
from .completions import show_completion_callback, install_completion_callback


@click.group()
@click.version_option(version=VERSION, prog_name="nnote")
@click.option(
    "--show-completion",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=show_completion_callback,
    help="Print the shell activation line for tab completion.",
)
@click.option(
    "--install-completion",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=install_completion_callback,
    help="Install tab completion for the current shell.",
)
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
cli.add_command(backup)
