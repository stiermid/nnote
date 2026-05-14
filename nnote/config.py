from __future__ import annotations

from .__version__ import APP_NAME
import os
import tempfile
import yaml
from pathlib import Path
from typing import Any


CONFIG_FILE_NAME = "config.yaml"
DEFAULT_NOTES_DIR = Path.home() / "nnotes"


def get_config_path() -> Path:
    """Return the config file path following XDG Base Directory spec."""
    config_home = Path.home() / ".config"
    return config_home / APP_NAME / CONFIG_FILE_NAME


class Config:
    def __init__(self, path: Path, data: dict[str, Any]):
        self._path = path
        self._data = data

    @classmethod
    def load(cls, path: Path | None = None) -> Config:
        """Load config file, creating the directory if needed."""
        path = path or get_config_path()
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            return cls(path, {})

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        if not isinstance(data, dict):
            raise ValueError("Config file must contain a dictionary at top level")

        return cls(path, data)

    def save(self) -> None:
        """Write current config data to disk atomically."""
        fd, tmp = tempfile.mkstemp(dir=self._path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                yaml.dump(self._data, f, default_flow_style=False, allow_unicode=True)
            Path(tmp).replace(self._path)
        except:
            os.unlink(tmp)
            raise

    _MISSING = object()

    def get(self, *keys: str, default: Any = None) -> Any:
        """Retrieve a nested value by key path, returning default if missing."""
        node = self._data
        for key in keys:
            if not isinstance(node, dict):
                return default
            node = node.get(key, self._MISSING)
            if node is self._MISSING:
                return default
        return node

    def set(self, *keys: str, value: Any) -> None:
        """Set a nested value by key path, creating intermediate dicts as needed."""
        node = self._data
        for key in keys[:-1]:
            node = node.setdefault(key, {})
        node[keys[-1]] = value

    @property
    def notes_dir(self) -> Path | None:
        raw = self.get("notes_dir")
        return Path(raw).expanduser() if raw is not None else None

    @property
    def editor(self) -> str | None:
        return self.get("editor") or os.environ.get("EDITOR")

    @property
    def backup_dir(self) -> Path | None:
        raw = self.get("backup_dir")
        return Path(raw).expanduser() if raw is not None else None
