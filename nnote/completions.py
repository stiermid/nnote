from pathlib import Path

import click
from click.shell_completion import (
    BashComplete,
    ZshComplete,
    FishComplete,
    CompletionItem,
)

from .config import Config

_SUPPORTED_SHELLS = {"bash", "zsh", "fish"}

_COMPLETION_FILE = {
    "bash": Path("~/.local/share/bash-completion/completions/nnote"),
    "zsh": Path("~/.local/share/zsh/site-functions/_nnote"),
    "fish": Path("~/.config/fish/completions/nnote.fish"),
}

_COMPLETE_CLASS = {
    "bash": BashComplete,
    "zsh": ZshComplete,
    "fish": FishComplete,
}


def _detect_shell():
    import os

    shell = Path(os.environ.get("SHELL", "")).name
    if shell not in _SUPPORTED_SHELLS:
        raise click.ClickException(f"Unsupported shell: {shell or '(unknown)'}")
    return shell


def _generate_script(shell, cli_obj):
    return _COMPLETE_CLASS[shell](cli_obj, {}, "nnote", "_NNOTE_COMPLETE").source()


def show_completion_callback(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    shell = _detect_shell()
    click.echo(_generate_script(shell, ctx.command))
    ctx.exit()


def install_completion_callback(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    shell = _detect_shell()
    script_file = _COMPLETION_FILE[shell].expanduser()
    if script_file.exists():
        click.echo(f"Completion already installed in {script_file}")
        ctx.exit()
    script_file.parent.mkdir(parents=True, exist_ok=True)
    script_file.write_text(_generate_script(shell, ctx.command))
    click.echo(f"Completion installed in {script_file}")
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
