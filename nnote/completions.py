from click.shell_completion import CompletionItem
from .config import Config


def complete_note_titles(ctx, param, incomplete):
    try:
        config = Config.load()
        directory = ctx.params.get("directory")
        root = config.notes_dir / directory if directory else config.notes_dir
        if not root or not root.exists():
            return []
        return [
            CompletionItem(p.name)
            for p in sorted(root.iterdir())
            if p.is_file() and p.name.startswith(incomplete)
        ]
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
