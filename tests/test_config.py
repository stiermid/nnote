import pytest
from pathlib import Path
from nnote.config import Config, get_config_path


def test_load_missing_file_returns_empty(tmp_path):
    config = Config.load(tmp_path / "config.yaml")
    assert config.notes_dir is None
    assert config._data == {}


def test_load_existing_file(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("notes_dir: /tmp/notes\neditor: vim\n")
    config = Config.load(cfg_file)
    assert config.get("editor") == "vim"


def test_load_invalid_file_raises(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("- not\n- a\n- dict\n")
    with pytest.raises(ValueError):
        Config.load(cfg_file)


def test_save_and_reload(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    config = Config.load(cfg_file)
    config.set("notes_dir", value="/tmp/nnotes")
    config.save()

    reloaded = Config.load(cfg_file)
    assert reloaded.get("notes_dir") == "/tmp/nnotes"


def test_get_missing_key_returns_default(tmp_path):
    config = Config.load(tmp_path / "config.yaml")
    assert config.get("missing") is None
    assert config.get("missing", default="fallback") == "fallback"


def test_get_explicit_null_value(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("key: null\n")
    config = Config.load(cfg_file)
    assert config.get("key") is None
    assert config.get("key", default="fallback") is None


def test_get_nested_key(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("a:\n  b: value\n")
    config = Config.load(cfg_file)
    assert config.get("a", "b") == "value"
    assert config.get("a", "missing") is None


def test_set_creates_nested_keys(tmp_path):
    config = Config.load(tmp_path / "config.yaml")
    config.set("a", "b", value="deep")
    assert config.get("a", "b") == "deep"


def test_notes_dir_property_expands_home(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("notes_dir: ~/nnotes\n")
    config = Config.load(cfg_file)
    assert config.notes_dir == Path.home() / "nnotes"


def test_notes_dir_none_when_not_set(tmp_path):
    config = Config.load(tmp_path / "config.yaml")
    assert config.notes_dir is None


def test_editor_falls_back_to_env(tmp_path, monkeypatch):
    monkeypatch.setenv("EDITOR", "nano")
    config = Config.load(tmp_path / "config.yaml")
    assert config.editor == "nano"


def test_editor_config_takes_priority_over_env(tmp_path, monkeypatch):
    monkeypatch.setenv("EDITOR", "nano")
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("editor: nvim\n")
    config = Config.load(cfg_file)
    assert config.editor == "nvim"


def test_editor_none_when_not_configured(tmp_path, monkeypatch):
    monkeypatch.delenv("EDITOR", raising=False)
    config = Config.load(tmp_path / "config.yaml")
    assert config.editor is None


def test_backup_dir_property_expands_home(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("backup_dir: ~/backups\n")
    config = Config.load(cfg_file)
    assert config.backup_dir == Path.home() / "backups"


def test_backup_dir_none_when_not_set(tmp_path):
    config = Config.load(tmp_path / "config.yaml")
    assert config.backup_dir is None


def test_get_config_path_uses_xdg_config_home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    assert get_config_path() == tmp_path / "nnote" / "config.yaml"


def test_get_config_path_falls_back_to_dot_config(monkeypatch):
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    assert get_config_path() == Path.home() / ".config" / "nnote" / "config.yaml"
