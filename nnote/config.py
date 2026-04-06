from __future__ import annotations

from .__version__ import APP_NAME
import yaml
from pathlib import Path
from typing import Any


CONFIG_FILE_NAME = "config.yaml"


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

    def get(self, *keys: str, default: Any = None) -> Any:
        """Retrieve a nested value by key path, returning default if missing."""
        node = self._data
        for key in keys:
            if not isinstance(node, dict):
                return default
            node = node.get(key, default)
            if node is default:
                return default
        return node
