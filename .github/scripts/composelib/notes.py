"""Edit note frontmatter textually and apply curation entries."""
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from . import ComposeError
from .tree import _walk

KEY_LINE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")
H1 = re.compile(r"^#\s+(.+)$")
POSITIVE_INT = re.compile(r"^[1-9][0-9]*$")
CURATION_KEYS = {"path", "featured", "summary", "publish", "blurb"}
SUMMARY_MAX = 160
BLURB_MAX = 400
QUOTED_KEYS = {"summary", "title", "blurb"}


def split_frontmatter(text: str) -> tuple[list[str] | None, str]:
    """Return (lines between the --- delimiters, body after), or (None, text) without frontmatter.

    CRLF is normalised to LF first, so the returned text is always LF.
    """
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None, text
    lines = text[4:].split("\n")
    for i, line in enumerate(lines):
        if line == "---":
            return lines[:i], "\n".join(lines[i + 1:])
    return None, text


def join_frontmatter(lines: list[str], body: str) -> str:
    return "".join(f"{line}\n" for line in ["---", *lines, "---"]) + body


def _find_key(lines: list[str], key: str) -> tuple[int, int] | None:
    """Span [start, end) of the key's line plus its continuation lines."""
    start = None
    for i, line in enumerate(lines):
        m = KEY_LINE.match(line)
        if start is not None and m:
            return start, i
        if start is None and m and m.group(1) == key:
            start = i
    return None if start is None else (start, len(lines))


def _raw_value(lines: list[str], key: str) -> str | None:
    span = _find_key(lines, key)
    return None if span is None else KEY_LINE.match(lines[span[0]]).group(2).strip()


def get_key(lines: list[str], key: str) -> str | None:
    """The key's scalar text with surrounding quotes removed."""
    raw = _raw_value(lines, key)
    if raw is None:
        return None
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        return re.sub(r'\\(["\\])', r"\1", raw[1:-1])
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1]
    return raw


def set_key(lines: list[str], key: str, value: str) -> list[str]:
    if key in QUOTED_KEYS:
        value = '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    new = f"{key}: {value}"
    span = _find_key(lines, key)
    if span is None:
        return [*lines, new]
    return [*lines[:span[0]], new, *lines[span[1]:]]


def drop_key(lines: list[str], key: str) -> list[str]:
    span = _find_key(lines, key)
    return list(lines) if span is None else [*lines[:span[0]], *lines[span[1]:]]


def first_h1(body: str) -> str | None:
    fenced = False
    for line in body.split("\n"):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced and (m := H1.match(line)):
            return m.group(1).strip()
    return None


def normalize_note(text: str, machine: str, created: str) -> str:
    """Fill the machine, publish and title keys; drop featured_candidate. `created` is YYYY-MM-DD."""
    lines, body = split_frontmatter(text)
    if lines is None:
        lines, body = ["tags: []", f"created: {created}", "publish: true"], text
    lines = drop_key(lines, "featured_candidate")
    if get_key(lines, "machine") is None:
        lines = set_key(lines, "machine", machine)
    if get_key(lines, "publish") is None:
        lines = set_key(lines, "publish", "true")
    if get_key(lines, "title") is None and (h1 := first_h1(body)):
        lines = set_key(lines, "title", h1)
    return join_frontmatter(lines, body)


@dataclass(frozen=True)
class CurationEntry:
    path: str
    featured: int | None = None
    summary: str | None = None
    publish: bool | None = None
    blurb: str | None = None


def load_curation(path: Path) -> list[CurationEntry]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        raise ComposeError(f"{path}: curation must be a list of entries")
    entries = []
    for item in data:
        if not isinstance(item, dict) or "path" not in item:
            raise ComposeError(f"{path}: every entry needs a path")
        for key in item:
            if key not in CURATION_KEYS:
                raise ComposeError(f"{item['path']}: unknown key {key}")
        entries.append(CurationEntry(item["path"], item.get("featured"),
                                     item.get("summary"), item.get("publish"),
                                     item.get("blurb")))
    return entries


def _inside_tree(path) -> bool:
    """False for absolute paths, any '..' segment, or a leading './'."""
    if not isinstance(path, str) or not path:
        return False
    return not (path.startswith(("/", "./")) or Path(path).is_absolute()
                or ".." in path.replace("\\", "/").split("/"))


def validate_curation(entries: list[CurationEntry], published_root: Path,
                      frontmatter_ranks: dict[str, int]) -> list[str]:
    """Error strings for the entries; an empty list means valid."""
    errors: list[str] = []
    seen: dict[int, str] = {}
    seen_paths: set[str] = set()
    for e in entries:
        if not _inside_tree(e.path):
            errors.append(f"{e.path}: path must be relative and inside the published tree")
            continue
        if e.path in seen_paths:
            errors.append(f"duplicate path: {e.path}")
        seen_paths.add(e.path)
        if not (Path(published_root) / e.path).is_file():
            errors.append(f"unknown path: {e.path}")
        if e.featured is not None:
            if isinstance(e.featured, bool) or not isinstance(e.featured, int) or e.featured < 1:
                errors.append(f"{e.path}: featured must be a positive integer, got {e.featured!r}")
            elif e.featured in seen:
                errors.append(f"duplicate rank {e.featured}: {seen[e.featured]}, {e.path}")
            else:
                seen[e.featured] = e.path
                for other, rank in frontmatter_ranks.items():
                    if rank == e.featured and other != e.path:
                        errors.append(f"rank {rank} already used by {other}")
        if e.summary is not None:
            if not isinstance(e.summary, str):
                errors.append(f"{e.path}: summary must be a string")
            elif len(e.summary) > SUMMARY_MAX:
                errors.append(f"summary too long ({len(e.summary)} > {SUMMARY_MAX}): {e.path}")
        if e.blurb is not None:
            if not isinstance(e.blurb, str):
                errors.append(f"{e.path}: blurb must be a string")
            elif len(e.blurb) > BLURB_MAX:
                errors.append(f"blurb too long ({len(e.blurb)} > {BLURB_MAX}): {e.path}")
        if e.publish is not None and not isinstance(e.publish, bool):
            errors.append(f"{e.path}: publish must be true or false")
    return errors


def apply_curation(text: str, entry: CurationEntry) -> str:
    """Set the keys the entry carries; leave the rest of the note alone."""
    lines, body = split_frontmatter(text)
    if lines is None:
        lines, body = [], text
    if entry.featured is not None:
        lines = set_key(lines, "featured", str(entry.featured))
    if entry.summary is not None:
        lines = set_key(lines, "summary", entry.summary)
    if entry.publish is not None:
        lines = set_key(lines, "publish", "true" if entry.publish else "false")
    if entry.blurb is not None:
        lines = set_key(lines, "blurb", entry.blurb)
    return join_frontmatter(lines, body)


def _featured_values(published_root: Path, paths: set[str]):
    """Yield (published path, raw featured text) for planned notes that have a featured key."""
    root = Path(published_root)
    for rel, full in _walk(root, [".git"]):
        if not rel.endswith(".md") or rel not in paths:
            continue
        lines, _ = split_frontmatter(full.read_text(encoding="utf-8", errors="replace"))
        raw = None if lines is None else _raw_value(lines, "featured")
        if raw is not None:
            yield rel, raw


def frontmatter_ranks(published_root: Path, mac_paths: set[str]) -> dict[str, int]:
    """{published path: rank} for Mac notes with a valid integer featured value."""
    return {rel: int(raw) for rel, raw in _featured_values(published_root, mac_paths)
            if POSITIVE_INT.match(raw)}


def rank_errors(published_root: Path, paths: set[str]) -> list[str]:
    """Bad featured values among the given published paths (the compose plan)."""
    return sorted(f"{rel}: featured must be an integer, got '{raw}'"
                  for rel, raw in _featured_values(published_root, paths) if not POSITIVE_INT.match(raw))
