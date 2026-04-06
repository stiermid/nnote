import pytest
from pathlib import Path
from nnote.search import search_notes, highlight, _score_title


# --- scoring unit tests ---

def test_score_exact_match():
    assert _score_title("todo", "todo") == 100


def test_score_prefix_match():
    assert _score_title("tod", "todo") == 70


def test_score_substring_match():
    assert _score_title("od", "todo") == 50


def test_score_fuzzy_match():
    score = _score_title("tdo", "todo")
    assert 0 < score < 50


def test_score_no_match():
    assert _score_title("xyz", "todo") == 0


def test_score_case_insensitive():
    assert _score_title("TODO", "todo") == 100


# --- search_notes integration tests ---

def test_finds_exact_title_match(tmp_path):
    (tmp_path / "todo").write_text("buy milk")
    results = search_notes(tmp_path, "todo")
    assert len(results) == 1
    assert results[0].rel_path == "todo"
    assert results[0].title_match is True


def test_finds_content_match(tmp_path):
    (tmp_path / "grocery").write_text("buy milk\nbuy eggs\n")
    results = search_notes(tmp_path, "milk")
    assert len(results) == 1
    assert results[0].title_match is False
    assert any("milk" in line for _, line in results[0].matching_lines)


def test_title_match_ranks_above_content_match(tmp_path):
    (tmp_path / "meeting").write_text("discuss budget")
    (tmp_path / "notes").write_text("meeting at 9am\nmeeting recap\nmeeting notes\n")
    results = search_notes(tmp_path, "meeting")
    assert results[0].rel_path == "meeting"


def test_no_results_for_unknown_query(tmp_path):
    (tmp_path / "todo").write_text("buy milk")
    results = search_notes(tmp_path, "xyzzy")
    assert results == []


def test_searches_subdirectories(tmp_path):
    subdir = tmp_path / "work"
    subdir.mkdir()
    (subdir / "standup").write_text("daily standup notes")
    results = search_notes(tmp_path, "standup")
    assert len(results) == 1
    assert results[0].rel_path == "work/standup"


def test_matching_lines_capped_at_three(tmp_path):
    content = "\n".join(f"line with keyword {i}" for i in range(10))
    (tmp_path / "note").write_text(content)
    results = search_notes(tmp_path, "keyword")
    assert len(results[0].matching_lines) == 3


def test_skips_unreadable_files(tmp_path):
    (tmp_path / "binary").write_bytes(bytes(range(256)))
    results = search_notes(tmp_path, "query")
    assert results == []


# --- highlight tests ---

def test_highlight_wraps_match():
    result = highlight("hello world", "world")
    assert "world" in result
    assert "\x1b[" in result  # ANSI escape present


def test_highlight_case_insensitive():
    result = highlight("Hello World", "world")
    assert "World" in result
    assert "\x1b[" in result


def test_highlight_no_match_unchanged():
    result = highlight("hello world", "xyz")
    assert result == "hello world"
