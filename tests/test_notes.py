import click
import pytest
from nnote.config import Config
from nnote.notes import resolve_note_path


def _config_with_notes_dir(tmp_path) -> Config:
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(f"notes_dir: {tmp_path / 'notes'}\n")
    return Config.load(cfg_file)


def test_resolve_note_path_no_directory(tmp_path):
    config = _config_with_notes_dir(tmp_path)
    path = resolve_note_path(config, "mytitle", None)
    assert path == config.notes_dir / "mytitle"


def test_resolve_note_path_with_directory(tmp_path):
    config = _config_with_notes_dir(tmp_path)
    path = resolve_note_path(config, "mytitle", "work")
    assert path == config.notes_dir / "work" / "mytitle"


def test_resolve_note_path_raises_when_notes_dir_not_set(tmp_path):
    config = Config.load(tmp_path / "config.yaml")
    with pytest.raises(click.ClickException):
        resolve_note_path(config, "mytitle", None)


def test_resolve_note_path_rejects_traversal_in_title(tmp_path):
    config = _config_with_notes_dir(tmp_path)
    with pytest.raises(click.ClickException, match="Invalid path"):
        resolve_note_path(config, "../../etc/passwd", None)


def test_resolve_note_path_rejects_traversal_in_directory(tmp_path):
    config = _config_with_notes_dir(tmp_path)
    with pytest.raises(click.ClickException, match="Invalid path"):
        resolve_note_path(config, "note", "../../etc")
