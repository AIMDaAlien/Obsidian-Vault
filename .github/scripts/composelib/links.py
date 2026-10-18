"""Fix wikilinks and embeds in prose: resolve bare image embeds, unwrap dead file links."""
import os
import re
from pathlib import Path

IMAGE_EXT = ("png", "svg", "jpg", "jpeg", "gif", "webp")
SKIP_DIRS = {".git", ".github"}

# groups: embed bang, target, #anchor, pipe (plain or escaped, kept verbatim), alias
WIKILINK_RE = re.compile(r"(!?)\[\[([^\]|#\\]+)(#[^\]|]*)?(?:(\\?\|)([^\]]*))?\]\]")
_FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.DOTALL)
_SIZE = re.compile(r"\d+(x\d+)?")


def _ext(name: str) -> str:
    base = name.rsplit("/", 1)[-1]
    return base.rsplit(".", 1)[-1].lower() if "." in base else ""


def _base(name: str) -> str:
    return name.rsplit("/", 1)[-1]


def build_index(published_root: Path) -> dict[str, list[str]]:
    """Lowercase basename -> sorted published relative paths, for every file."""
    index: dict[str, list[str]] = {}
    root = Path(published_root)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            rel = (Path(dirpath) / name).relative_to(root).as_posix()
            index.setdefault(name.lower(), []).append(rel)
    return {k: sorted(v) for k, v in index.items()}


def _split_fences(text: str):
    """Yield (is_code, chunk) for fenced blocks and the prose between them."""
    prose: list[str] = []
    code: list[str] = []
    fence = None
    for line in text.splitlines(keepends=True):
        if fence is None:
            m = _FENCE_OPEN.match(line)
            if m:
                if prose:
                    yield False, "".join(prose)
                    prose = []
                fence = m.group(1)
                code = [line]
            else:
                prose.append(line)
        else:
            code.append(line)
            s = line.strip()
            if s and s[0] == fence[0] and s == s[0] * len(s) and len(s) >= len(fence):
                yield True, "".join(code)
                fence = None
    if fence is not None:
        yield True, "".join(code)
    if prose:
        yield False, "".join(prose)


def _map_prose(text: str, fn) -> str:
    """Apply fn to prose only; fenced blocks and inline code spans pass through."""
    out = []
    for is_code, chunk in _split_fences(text):
        if is_code:
            out.append(chunk)
            continue
        pos = 0
        for m in _INLINE_CODE.finditer(chunk):
            out.append(fn(chunk[pos:m.start()]))
            out.append(m.group(0))
            pos = m.end()
        out.append(fn(chunk[pos:]))
    return "".join(out)


def resolve_bare_embeds(text, index, image_ext=IMAGE_EXT):
    """Rewrite ![[name.png]] to its full published path when exactly one file matches.

    Returns (text, unresolved) where unresolved holds 'name (ambiguous: ...)' or 'name (missing)'.
    """
    unresolved: list[str] = []

    def sub(m):
        bang, target, anchor, pipe, alias = m.groups()
        name = target.strip()
        if not bang or "/" in name or _ext(name) not in image_ext:
            return m.group(0)
        hits = index.get(name.lower(), [])
        if len(hits) == 1:
            tail = (anchor or "") + (pipe + alias if pipe else "")
            return f"![[{hits[0]}{tail}]]"
        unresolved.append(f"{name} (ambiguous: {', '.join(hits)})" if hits else f"{name} (missing)")
        return m.group(0)

    return _map_prose(text, lambda s: WIKILINK_RE.sub(sub, s)), unresolved


def unwrap_excluded_links(text, index, exclude_ext, image_ext=IMAGE_EXT):
    """Replace links to excluded-extension files, or images missing from the index, with display text.

    Returns (text, unwrapped targets in document order).
    """
    unwrapped: list[str] = []

    def sub(m):
        bang, target, _anchor, _pipe, alias = m.groups()
        name = target.strip()
        ext = _ext(name)
        dead = ext in exclude_ext or (ext in image_ext and _base(name).lower() not in index)
        if not dead:
            return m.group(0)
        unwrapped.append(name)
        if alias is not None and alias.strip() and not (bang and _SIZE.fullmatch(alias.strip())):
            return alias
        base = _base(name)
        return base[: -(len(ext) + 1)]

    return _map_prose(text, lambda s: WIKILINK_RE.sub(sub, s)), unwrapped
