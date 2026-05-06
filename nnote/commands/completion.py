import click


_ACTIVATION = {
    "bash": 'eval "$(_NNOTE_COMPLETE=bash_source nnote)"',
    "zsh": 'eval "$(_NNOTE_COMPLETE=zsh_source nnote)"',
    "fish": "eval (env _NNOTE_COMPLETE=fish_source nnote)",
}


@click.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell):
    """Print shell completion setup instructions."""
    click.echo(f"Add this to your shell config:\n\n  {_ACTIVATION[shell]}")
