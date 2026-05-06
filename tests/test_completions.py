from pathlib import Path
from unittest.mock import patch

import pytest
from click.shell_completion import CompletionItem

from nnote.completions import complete_note_titles, complete_directories
from nnote.config import Config


class _FakeCtx:
    def __init__(self, params=None):
        self.params = params or {}


def _config_with_notes_dir(tmp_path) -> Config:
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(f"notes_dir: {tmp_path / 'notes'}\n")
    return Config.load(cfg_file)


def _make_notes(notes_dir: Path, files, dirs=()):
    notes_dir.mkdir(parents=True, exist_ok=True)
    for name in files:
        (notes_dir / name).touch()
    for name in dirs:
        (notes_dir / name).mkdir()


@pytest.fixture
def cfg(tmp_path):
    return _config_with_notes_dir(tmp_path)


def test_complete_note_titles_returns_matching_files(cfg):
    _make_notes(cfg.notes_dir, ["alpha", "beta", "another"])
    with patch("nnote.completions.Config.load", return_value=cfg):
        results = complete_note_titles(_FakeCtx(), None, "a")
    names = [r.value for r in results]
    assert "alpha" in names
    assert "another" in names
    assert "beta" not in names


def test_complete_note_titles_empty_prefix_returns_files_and_dirs(cfg):
    _make_notes(cfg.notes_dir, ["x", "y"], dirs=["subdir"])
    with patch("nnote.completions.Config.load", return_value=cfg):
        results = complete_note_titles(_FakeCtx(), None, "")
    assert {r.value for r in results} == {"x", "y", "subdir/"}


def test_complete_note_titles_respects_directory_flag(cfg):
    subdir = cfg.notes_dir / "work"
    _make_notes(subdir, ["report", "review"])
    _make_notes(cfg.notes_dir, ["readme"])
    with patch("nnote.completions.Config.load", return_value=cfg):
        results = complete_note_titles(_FakeCtx({"directory": "work"}), None, "")
    names = {r.value for r in results}
    assert names == {"report", "review"}
    assert "readme" not in names


def test_complete_note_titles_path_style(cfg):
    subdir = cfg.notes_dir / "work"
    _make_notes(subdir, ["report", "review"])
    with patch("nnote.completions.Config.load", return_value=cfg):
        results = complete_note_titles(_FakeCtx(), None, "work/re")
    assert {r.value for r in results} == {"work/report", "work/review"}


def test_complete_note_titles_path_style_dir_prefix(cfg):
    _make_notes(cfg.notes_dir, [], dirs=["work", "personal"])
    with patch("nnote.completions.Config.load", return_value=cfg):
        results = complete_note_titles(_FakeCtx(), None, "w")
    assert {r.value for r in results} == {"work/"}


def test_complete_directories_returns_subdirs(cfg):
    _make_notes(cfg.notes_dir, ["note"], dirs=["work", "personal"])
    with patch("nnote.completions.Config.load", return_value=cfg):
        results = complete_directories(_FakeCtx(), None, "")
    names = {r.value for r in results}
    assert names == {"work", "personal"}
    assert "note" not in names


def test_complete_directories_filters_by_prefix(cfg):
    _make_notes(cfg.notes_dir, [], dirs=["work", "personal", "projects"])
    with patch("nnote.completions.Config.load", return_value=cfg):
        results = complete_directories(_FakeCtx(), None, "p")
    names = {r.value for r in results}
    assert names == {"personal", "projects"}
    assert "work" not in names


def test_complete_note_titles_missing_notes_dir_returns_empty(tmp_path):
    cfg = Config.load(tmp_path / "config.yaml")
    with patch("nnote.completions.Config.load", return_value=cfg):
        results = complete_note_titles(_FakeCtx(), None, "")
    assert results == []


def test_complete_note_titles_exception_returns_empty():
    with patch("nnote.completions.Config.load", side_effect=RuntimeError("boom")):
        results = complete_note_titles(_FakeCtx(), None, "")
    assert results == []
