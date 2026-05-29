import subprocess
import click
from pathlib import Path
from .config import Config


def resolve_note_path(config: Config, title: str, directory: str | None) -> Path:
    if config.notes_dir is None:
        raise click.ClickException(
            "Notes directory not configured. Run `nnote init` first."
        )
    base = config.notes_dir / directory if directory else config.notes_dir
    resolved = (base / title).resolve()
    notes_root = config.notes_dir.resolve()
    if not resolved.is_relative_to(notes_root):
        raise click.ClickException("Invalid path: must stay within notes directory.")
    return resolved


def open_in_editor(config: Config, path: Path) -> None:
    if config.editor is None:
        raise click.ClickException(
            "No editor configured. Set 'editor' in config or the $EDITOR environment variable."
        )
    subprocess.run([config.editor, str(path)], check=False)
