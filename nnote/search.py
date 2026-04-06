import difflib
import click
from dataclasses import dataclass, field
from pathlib import Path


_TITLE_EXACT        = 100
_TITLE_PREFIX       =  70
_TITLE_SUBSTR       =  50
_FUZZY_THRESHOLD    = 0.6
_FUZZY_WEIGHT       =  40
_CONTENT_LINE_SCORE =  10
_CONTENT_MAX_LINES  =   3


@dataclass
class SearchResult:
    rel_path: str
    score: float
    title_match: bool
    matching_lines: list[tuple[int, str]] = field(default_factory=list)


def _score_title(query: str, name: str) -> float:
    q, n = query.lower(), name.lower()
    if q == n:
        return _TITLE_EXACT
    if n.startswith(q):
        return _TITLE_PREFIX
    if q in n:
        return _TITLE_SUBSTR
    ratio = difflib.SequenceMatcher(None, q, n).ratio()
    if ratio >= _FUZZY_THRESHOLD:
        return ratio * _FUZZY_WEIGHT
    return 0.0


def search_notes(root: Path, query: str) -> list[SearchResult]:
    results: list[SearchResult] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        rel = str(path.relative_to(root))
        title_score = _score_title(query, path.name)

        matching_lines: list[tuple[int, str]] = []
        try:
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if query.lower() in line.lower():
                    matching_lines.append((lineno, line.strip()))
        except (UnicodeDecodeError, OSError):
            pass

        content_score = min(
            len(matching_lines) * _CONTENT_LINE_SCORE,
            _CONTENT_LINE_SCORE * _CONTENT_MAX_LINES,
        )
        total = title_score + content_score

        if total > 0:
            results.append(SearchResult(
                rel_path=rel,
                score=total,
                title_match=title_score > 0,
                matching_lines=matching_lines[:_CONTENT_MAX_LINES],
            ))

    results.sort(key=lambda r: r.score, reverse=True)
    return results


def highlight(text: str, query: str) -> str:
    lower = text.lower()
    q = query.lower()
    out, i = "", 0
    while i < len(text):
        if lower[i:i + len(q)] == q:
            out += click.style(text[i:i + len(q)], bold=True, fg="yellow")
            i += len(q)
        else:
            out += text[i]
            i += 1
    return out
