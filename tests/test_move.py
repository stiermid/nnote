import pytest
from unittest.mock import patch
from click.testing import CliRunner
from nnote.cli import cli
from nnote.config import Config


@pytest.fixture
def env(tmp_path):
    notes_dir = tmp_path / "notes"
    notes_dir.mkdir()
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(f"notes_dir: {notes_dir}\n")
    cfg = Config.load(cfg_file)
    return cfg, notes_dir


def invoke(cfg, *args):
    with patch("nnote.commands.move.Config") as MockConfig:
        MockConfig.load.return_value = cfg
        return CliRunner().invoke(cli.commands["move"], list(args))


# ── happy paths ────────────────────────────────────────────────────────────────


def test_rename_note(env):
    cfg, notes_dir = env
    (notes_dir / "old").write_text("content")

    invoke(cfg, "old", "new")

    assert not (notes_dir / "old").exists()
    assert (notes_dir / "new").read_text() == "content"


def test_move_to_different_directory(env):
    cfg, notes_dir = env
    (notes_dir / "note").write_text("hi")

    invoke(cfg, "note", "--dest-dir", "work")

    assert not (notes_dir / "note").exists()
    assert (notes_dir / "work" / "note").exists()


def test_move_and_rename(env):
    cfg, notes_dir = env
    (notes_dir / "old").write_text("data")

    invoke(cfg, "old", "new", "--dest-dir", "archive")

    assert not (notes_dir / "old").exists()
    assert (notes_dir / "archive" / "new").exists()


def test_move_from_subdirectory(env):
    cfg, notes_dir = env
    src = notes_dir / "work"
    src.mkdir()
    (src / "note").write_text("work note")

    invoke(cfg, "note", "-d", "work", "--dest-dir", "personal")

    assert not (src / "note").exists()
    assert (notes_dir / "personal" / "note").exists()


def test_dest_dir_created_if_missing(env):
    cfg, notes_dir = env
    (notes_dir / "note").write_text("x")

    invoke(cfg, "note", "--dest-dir", "brand-new")

    assert (notes_dir / "brand-new" / "note").exists()


# ── error paths ────────────────────────────────────────────────────────────────


def test_error_source_not_found(env):
    cfg, _ = env
    r = invoke(cfg, "ghost", "new")
    assert r.exit_code != 0
    assert "not found" in r.output.lower()


def test_error_dest_already_exists(env):
    cfg, notes_dir = env
    (notes_dir / "a").write_text("a")
    (notes_dir / "b").write_text("b")

    r = invoke(cfg, "a", "b")
    assert r.exit_code != 0
    assert "already exists" in r.output.lower()


def test_error_source_and_dest_are_same(env):
    cfg, notes_dir = env
    (notes_dir / "note").write_text("x")

    r = invoke(cfg, "note", "note")
    assert r.exit_code != 0
    assert "same" in r.output.lower()


def test_error_no_dest_given(env):
    cfg, notes_dir = env
    (notes_dir / "note").write_text("x")

    r = invoke(cfg, "note")
    assert r.exit_code != 0
