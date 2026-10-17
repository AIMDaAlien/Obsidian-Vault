#!/usr/bin/env python3
"""Generate garden-manifest.json from vault markdown files.

Walks all .md files, parses YAML frontmatter with a small stdlib parser,
and builds a manifest with a file/directory tree, a metadata map (every
frontmatter key plus title and updated) and a wikilink map.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

SKIP_DIRS = {'.git', '.obsidian', '.stfolder', '.github'}

FRONTMATTER_RE = re.compile(r'\A---[ \t]*\n(.*?)^---[ \t]*$\n?', re.DOTALL | re.MULTILINE)
KEY_VALUE_RE = re.compile(r'^([A-Za-z0-9_-]+):[ \t]*(.*)$')
LIST_ITEM_RE = re.compile(r'^[ \t]*-[ \t]+(.*)$')
INTEGER_RE = re.compile(r'^-?\d+$')
FENCE_RE = re.compile(r'^(```|~~~).*?^\1[^\n]*$', re.DOTALL | re.MULTILINE)
WIKILINK_RE = re.compile(r'(!?)\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]')
FILE_EXTENSION_RE = re.compile(r'\.\w{2,5}$')
H1_RE = re.compile(r'^#[ \t]+(.+?)[ \t]*$', re.MULTILINE)


def load_gitignore_dirs(repo_root):
    """Parse .gitignore for directory patterns to exclude."""
    gitignore = os.path.join(repo_root, '.gitignore')
    ignored = set()
    if not os.path.exists(gitignore):
        return ignored
    with open(gitignore, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().strip('/')
            if not line or line.startswith('#'):
                continue
            # Treat each non-glob entry as a potential directory name
            if '*' not in line and '?' not in line:
                ignored.add(line)
    return ignored


def unquote(value):
    """Strip one pair of matching surrounding quotes."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in '"\'':
        return value[1:-1]
    return value


def parse_scalar(raw):
    """Convert a frontmatter value to bool, None, int, list or string."""
    value = raw.strip()
    if value.startswith('[') and value.endswith(']'):
        items = [unquote(item.strip()) for item in value[1:-1].split(',')]
        return [item for item in items if item]
    lowered = value.lower()
    if lowered == 'true':
        return True
    if lowered == 'false':
        return False
    if lowered == 'null':
        return None
    if INTEGER_RE.match(value):
        return int(value)
    return unquote(value)


def parse_frontmatter(text):
    """Split text into (frontmatter dict, body). Malformed lines are skipped."""
    text = text.replace('\r\n', '\n')
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    fm = {}
    list_key = None  # key awaiting block-list items
    for line in match.group(1).split('\n'):
        item = LIST_ITEM_RE.match(line)
        if item and list_key is not None:
            if not isinstance(fm[list_key], list):
                fm[list_key] = []
            fm[list_key].append(unquote(item.group(1).strip()))
            continue
        pair = KEY_VALUE_RE.match(line)
        if not pair:
            continue
        key, raw = pair.groups()
        fm[key] = parse_scalar(raw) if raw.strip() else None
        list_key = key if not raw.strip() else None
    return fm, text[match.end():]


def extract_title(fm, body, filename):
    """Frontmatter title, else first H1, else the filename stem."""
    title = fm.get('title')
    if isinstance(title, str) and title.strip():
        return title.strip()
    h1 = H1_RE.search(FENCE_RE.sub('', body))
    if h1:
        return h1.group(1)
    return os.path.splitext(os.path.basename(filename))[0]


def extract_links(body):
    """Wikilink targets, deduplicated, order preserved.

    Links inside fenced code blocks and file embeds (![[x.png]]) are ignored.
    """
    links = []
    for embed, target in WIKILINK_RE.findall(FENCE_RE.sub('', body)):
        target = target.strip()
        if embed and FILE_EXTENSION_RE.search(target):
            continue
        if target and target not in links:
            links.append(target)
    return links


def git_last_commit_date(repo_root, rel_path):
    """Date (YYYY-MM-DD) of the last commit touching rel_path, or None."""
    try:
        result = subprocess.run(
            ['git', '-C', repo_root, '--literal-pathspecs', 'log', '-1', '--format=%cs', '--', rel_path],
            capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def should_skip(parts):
    """Check if any path component is in the skip set or hidden."""
    return any(p in SKIP_DIRS or p.startswith('.') for p in parts)


def build_manifest(repo_root):
    """Walk repo_root and return the manifest dict."""
    repo_root = os.path.abspath(repo_root)
    skip_all = SKIP_DIRS | load_gitignore_dirs(repo_root)
    tree, metadata, links = [], {}, {}

    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = sorted(d for d in dirnames if d not in skip_all and not d.startswith('.'))
        rel_dir = os.path.relpath(dirpath, repo_root)
        if rel_dir == '.':
            rel_dir = ''
        elif not should_skip(rel_dir.split(os.sep)):
            tree.append({'path': rel_dir, 'type': 'dir'})

        for fname in sorted(filenames):
            rel_path = os.path.join(rel_dir, fname) if rel_dir else fname
            if not fname.endswith('.md') or should_skip(rel_path.split(os.sep)):
                continue
            tree.append({'path': rel_path, 'type': 'file'})

            try:
                with open(os.path.join(dirpath, fname), 'r', encoding='utf-8-sig', errors='replace') as f:
                    text = f.read()
            except OSError:
                continue
            fm, body = parse_frontmatter(text)
            fm['title'] = extract_title(fm, body, fname)
            if not (isinstance(fm.get('updated'), str) and fm['updated']):
                fm.pop('updated', None)
                updated = git_last_commit_date(repo_root, rel_path)
                if updated:
                    fm['updated'] = updated
            metadata[rel_path] = fm
            note_links = extract_links(body)
            if note_links:
                links[rel_path] = note_links

    return {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'tree': tree,
        'metadata': metadata,
        'links': links,
    }


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    repo_root = os.path.abspath(argv[0] if argv else '.')
    manifest = build_manifest(repo_root)

    with open(os.path.join(repo_root, 'garden-manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    tree, metadata, links = manifest['tree'], manifest['metadata'], manifest['links']
    files = sum(1 for e in tree if e['type'] == 'file')
    dirs = sum(1 for e in tree if e['type'] == 'dir')
    publishable = sum(1 for v in metadata.values() if v.get('publish') is True)
    total_links = sum(len(v) for v in links.values())
    print(f'Manifest generated: {files} files, {dirs} dirs, {publishable} publishable notes, '
          f'{total_links} links across {len(links)} notes')
    return 0


if __name__ == '__main__':
    sys.exit(main())
