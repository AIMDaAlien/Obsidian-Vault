"""Plan and apply the published file tree from the source vaults."""
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from . import ComposeError
from .config import Config, Source

WIKI_EMBED = re.compile(r"!\[\[([^\]|#]+)")
MD_EMBED = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")

# Syncthing metadata: never published, counted or scanned, whatever compose.yml says.
SYNCTHING_DIRS = (".stfolder", ".stversions")
SYNCTHING_FILES = (".stignore",)


@dataclass(frozen=True)
class TreeStats:
    added: int
    changed: int
    removed: int


def _walk(root: Path, exclude_dirs: list[str], skip_symlinks: bool = False,
          exclude_files: tuple[str, ...] | list[str] = ()):
    """Yield (relative posix path, absolute path) of files outside excluded dirs.

    skip_symlinks is for source vaults: a symlink must never publish what it points at.
    exclude_files are file names skipped at any depth.
    """
    skip = set(exclude_dirs)
    skip_files = set(exclude_files)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in filenames:
            if name in skip_files:
                continue
            full = Path(dirpath) / name
            if skip_symlinks and full.is_symlink():
                continue
            yield full.relative_to(root).as_posix(), full


def _source_walk(root: Path, cfg: Config):
    """Walk a source vault: config exclusions plus Syncthing metadata, no symlinks."""
    return _walk(root, [*cfg.exclude_dirs, *SYNCTHING_DIRS], skip_symlinks=True,
                 exclude_files=(*cfg.exclude_files, *SYNCTHING_FILES))


def _ext(rel: str) -> str:
    return rel.rsplit(".", 1)[-1].lower() if "." in rel.rsplit("/", 1)[-1] else ""


def _embedded_names(src: Source, cfg: Config) -> set[str]:
    """Basenames of everything the source's notes embed with ![[..]] or ![](..)."""
    names: set[str] = set()
    for rel, full in _source_walk(src.path, cfg):
        if _ext(rel) != "md":
            continue
        text = full.read_text(encoding="utf-8", errors="replace")
        for target in WIKI_EMBED.findall(text) + MD_EMBED.findall(text):
            names.add(unquote(target).strip().replace("\\", "/").rsplit("/", 1)[-1])
    return names


def _published_path(rel: str, src: Source) -> str:
    for old, new in src.path_map.items():
        if rel.startswith(old):
            return new + rel[len(old):]
    return rel


def _is_git(rel: str) -> bool:
    return rel == ".git" or rel.startswith(".git/")


def _scan(cfg: Config) -> tuple[dict[str, tuple[str, Path]], list[str]]:
    plan: dict[str, tuple[str, Path]] = {}
    clashes: set[str] = set()
    skipped: list[str] = []
    for src in cfg.sources:
        embedded = _embedded_names(src, cfg) if src.attachments else set()
        prefix = src.attachments.strip("/") + "/" if src.attachments else None
        for rel, full in _source_walk(src.path, cfg):
            ext = _ext(rel)
            if ext in cfg.exclude_ext:
                continue
            if prefix and rel.startswith(prefix):
                if ext not in cfg.image_ext or full.name not in embedded:
                    continue
            out = _published_path(rel, src)
            if _is_git(out) or _is_protected(out, cfg):
                skipped.append(out)
                continue
            if out in plan:
                clashes.add(out)
            else:
                plan[out] = (src.name, full)
    if clashes:
        raise ComposeError("collision:\n" + "\n".join(sorted(clashes)))
    return plan, sorted(skipped)


def plan_tree(cfg: Config) -> dict[str, tuple[str, Path]]:
    """Map each published relative path to (source name, source file).

    Source files that would land on a protected or .git path are left out;
    skipped_protected lists them.
    """
    return _scan(cfg)[0]


def skipped_protected(cfg: Config) -> list[str]:
    """Published paths that source files were dropped from because they are protected or .git."""
    return _scan(cfg)[1]


def _is_protected(rel: str, cfg: Config) -> bool:
    return any(rel == p or (p.endswith("/") and rel.startswith(p)) for p in cfg.protected)


def _differs(src: Path, dst: Path) -> bool:
    a, b = src.stat(), dst.stat()
    return a.st_size != b.st_size or int(a.st_mtime) != int(b.st_mtime)


def apply_tree(plan: dict[str, tuple[str, Path]], cfg: Config) -> TreeStats:
    """Copy new and changed files, delete stale unprotected ones, prune empty dirs."""
    root = cfg.published
    root.mkdir(parents=True, exist_ok=True)
    added = changed = removed = 0
    for rel, (_, src) in plan.items():
        dst = root / rel
        if not dst.exists():
            added += 1
        elif _differs(src, dst):
            changed += 1
        else:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    for rel, full in _walk(root, [".git"]):
        if _is_git(rel):
            continue
        if rel not in plan and not _is_protected(rel, cfg):
            full.unlink()
            removed += 1
    for dirpath, dirnames, _ in os.walk(root, topdown=False):
        rel = Path(dirpath).relative_to(root).as_posix()
        if rel == "." or _is_git(rel):
            continue
        if not os.listdir(dirpath):
            os.rmdir(dirpath)
    return TreeStats(added, changed, removed)


DEFAULT_EXCLUDE_DIRS = ["_inbox", ".obsidian", ".trash", "_private"]


def count_notes(path: Path, exclude_dirs: list[str] | None = None) -> int:
    """Markdown files under path, outside excluded dirs and Syncthing metadata."""
    skip = DEFAULT_EXCLUDE_DIRS if exclude_dirs is None else exclude_dirs
    return sum(1 for rel, _ in _walk(Path(path), [*skip, *SYNCTHING_DIRS], exclude_files=SYNCTHING_FILES)
               if _ext(rel) == "md")


def guard_sources(cfg: Config, last_counts: dict[str, int]) -> None:
    """Refuse to run when a source looks gone, empty or suddenly much smaller."""
    for src in cfg.sources:
        last = last_counts.get(src.name, 0)
        n = count_notes(src.path, cfg.exclude_dirs) if src.path.is_dir() else 0
        if n == 0 or n < last / 2:
            raise ComposeError(f"source looks empty: {src.name} ({n} notes, last {last})")
