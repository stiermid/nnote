from click.shell_completion import CompletionItem
from .config import Config


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
