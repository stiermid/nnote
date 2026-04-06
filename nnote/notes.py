import subprocess
import click
from pathlib import Path
from .config import Config


def resolve_note_path(config: Config, title: str, directory: str | None) -> Path:
    if config.notes_dir is None:
        raise click.ClickException("Notes directory not configured. Run `nnote init` first.")
    base = config.notes_dir / directory if directory else config.notes_dir
    return base / title


def open_in_editor(config: Config, path: Path) -> None:
    if config.editor is None:
        raise click.ClickException(
            "No editor configured. Set 'editor' in config or the $EDITOR environment variable."
        )
    subprocess.call([config.editor, str(path)])
