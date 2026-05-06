from pathlib import Path

import click
from click.shell_completion import CompletionItem

from .config import Config

_ACTIVATION_LINE = {
    "bash": 'eval "$(_NNOTE_COMPLETE=bash_source nnote)"',
    "zsh": 'eval "$(_NNOTE_COMPLETE=zsh_source nnote)"',
    "fish": "eval (env _NNOTE_COMPLETE=fish_source nnote)",
}

_SHELL_CONFIG = {
    "bash": Path("~/.bashrc"),
    "zsh": Path("~/.zshrc"),
    "fish": Path("~/.config/fish/config.fish"),
}


def _detect_shell():
    import shellingham

    shell, _ = shellingham.detect_shell()
    if shell not in _ACTIVATION_LINE:
        raise click.ClickException(f"Unsupported shell: {shell}")
    return shell


def show_completion_callback(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    shell = _detect_shell()
    click.echo(_ACTIVATION_LINE[shell])
    ctx.exit()


def install_completion_callback(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    shell = _detect_shell()
    line = _ACTIVATION_LINE[shell]
    config_file = _SHELL_CONFIG[shell].expanduser()
    if config_file.exists() and line in config_file.read_text():
        click.echo(f"Completion already installed in {config_file}")
        ctx.exit()
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with config_file.open("a") as f:
        f.write(f"\n{line}\n")
    click.echo(f"Completion installed in {config_file}")
    ctx.exit()


def complete_note_titles(ctx, param, incomplete):
    try:
        config = Config.load()
        root = config.notes_dir
        if not root or not root.exists():
            return []

        # Path-style input ("dir1/note") — split on last slash
        if "/" in incomplete:
            dir_part, name_part = incomplete.rsplit("/", 1)
            search_dir = root / dir_part
            value_prefix = dir_part + "/"
        else:
            directory = ctx.params.get("directory")
            search_dir = root / directory if directory else root
            value_prefix = ""
            name_part = incomplete

        if not search_dir.exists():
            return []

        results = []
        for p in sorted(search_dir.iterdir()):
            if not p.name.startswith(name_part):
                continue
            if p.is_file():
                results.append(CompletionItem(value_prefix + p.name))
            elif p.is_dir():
                results.append(CompletionItem(value_prefix + p.name + "/"))
        return results
    except Exception:
        return []


def complete_directories(ctx, param, incomplete):
    try:
        config = Config.load()
        root = config.notes_dir
        if not root or not root.exists():
            return []
        return [
            CompletionItem(p.name)
            for p in sorted(root.iterdir())
            if p.is_dir() and p.name.startswith(incomplete)
        ]
    except Exception:
        return []
