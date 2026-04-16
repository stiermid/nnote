import tarfile
from datetime import date
from unittest.mock import patch

import pytest
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
    with patch("nnote.commands.backup.Config") as MockConfig:
        MockConfig.load.return_value = cfg
        return CliRunner().invoke(cli.commands["backup"], list(args))


# ── happy paths ────────────────────────────────────────────────────────────────

def test_backup_creates_archive(env, tmp_path):
    cfg, notes_dir = env
    (notes_dir / "note1").write_text("hello")
    (notes_dir / "note2").write_text("world")

    out = tmp_path / "backup.tar.gz"
    r = invoke(cfg, str(out))

    assert r.exit_code == 0
    assert out.exists()
    with tarfile.open(out, "r:gz") as tar:
        names = tar.getnames()
    assert any("note1" in n for n in names)
    assert any("note2" in n for n in names)


def test_backup_scoped_to_directory(env, tmp_path):
    cfg, notes_dir = env
    sub = notes_dir / "work"
    sub.mkdir()
    (sub / "work-note").write_text("work")
    (notes_dir / "personal-note").write_text("personal")

    out = tmp_path / "backup.tar.gz"
    r = invoke(cfg, str(out), "-d", "work")

    assert r.exit_code == 0
    with tarfile.open(out, "r:gz") as tar:
        names = tar.getnames()
    assert any("work-note" in n for n in names)
    assert not any("personal-note" in n for n in names)


def test_backup_include_config(env, tmp_path):
    cfg, notes_dir = env
    (notes_dir / "note").write_text("hi")
    fake_config = tmp_path / "config.yaml"
    fake_config.write_text("notes_dir: /tmp/notes\n")

    out = tmp_path / "backup.tar.gz"
    with patch("nnote.commands.backup.Config") as MockConfig, \
         patch("nnote.commands.backup.Path") as MockPath:
        MockConfig.load.return_value = cfg
        # Patch the config path construction inside backup
        real_path = __import__("pathlib").Path
        def path_side_effect(*args):
            if args == ("~/.config/nnote/config.yaml",):
                p = real_path(fake_config)
                p_expanded = real_path(fake_config)
                # return a mock that .expanduser() returns real fake_config path
                class FakeConfigPath:
                    def expanduser(self):
                        return real_path(fake_config)
                return FakeConfigPath()
            return real_path(*args)
        MockPath.side_effect = path_side_effect
        MockPath.cwd = real_path.cwd

        r = CliRunner().invoke(cli.commands["backup"], [str(out), "--include-config"])

    assert r.exit_code == 0
    with tarfile.open(out, "r:gz") as tar:
        names = tar.getnames()
    assert "config.yaml" in names


def test_backup_dry_run_no_file_created(env, tmp_path):
    cfg, notes_dir = env
    (notes_dir / "note1").write_text("a")
    (notes_dir / "note2").write_text("b")

    out = tmp_path / "backup.tar.gz"
    r = invoke(cfg, str(out), "--dry-run")

    assert r.exit_code == 0
    assert not out.exists()
    assert "note1" in r.output
    assert "note2" in r.output
    assert "2 file(s) would be backed up" in r.output


def test_backup_quiet_suppresses_output(env, tmp_path):
    cfg, notes_dir = env
    (notes_dir / "note").write_text("x")

    out = tmp_path / "backup.tar.gz"
    r = invoke(cfg, str(out), "--quiet")

    assert r.exit_code == 0
    assert out.exists()
    assert r.output.strip() == ""


def test_backup_default_filename_uses_today(env, tmp_path):
    cfg, notes_dir = env
    (notes_dir / "note").write_text("x")

    today = date.today().isoformat()
    expected_name = f"nnote-backup-{today}.tar.gz"

    with patch("nnote.commands.backup.Config") as MockConfig, \
         patch("nnote.commands.backup.Path") as MockPath:
        MockConfig.load.return_value = cfg
        real_path = __import__("pathlib").Path
        created_paths = []

        def path_side_effect(*args):
            if args == ("~/.config/nnote/config.yaml",):
                class FakeConfigPath:
                    def expanduser(self):
                        return real_path("/nonexistent/config.yaml")
                return FakeConfigPath()
            p = real_path(*args)
            created_paths.append(p)
            return p

        MockPath.side_effect = path_side_effect
        MockPath.cwd = lambda: tmp_path

        r = CliRunner().invoke(cli.commands["backup"], [])

    assert r.exit_code == 0
    assert (tmp_path / expected_name).exists()


def test_backup_output_message(env, tmp_path):
    cfg, notes_dir = env
    (notes_dir / "note").write_text("x")

    out = tmp_path / "backup.tar.gz"
    r = invoke(cfg, str(out))

    assert r.exit_code == 0
    assert "1 file(s)" in r.output
    assert str(out) in r.output


# ── error paths ────────────────────────────────────────────────────────────────

def test_error_notes_dir_not_configured(tmp_path):
    cfg = Config(tmp_path / "config.yaml", {})
    r = invoke(cfg, str(tmp_path / "out.tar.gz"))
    assert r.exit_code != 0
    assert "not configured" in r.output.lower()


def test_error_scoped_directory_not_found(env, tmp_path):
    cfg, notes_dir = env
    r = invoke(cfg, str(tmp_path / "out.tar.gz"), "-d", "ghost")
    assert r.exit_code != 0
    assert "not found" in r.output.lower()
