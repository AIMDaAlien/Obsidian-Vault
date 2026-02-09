#!/usr/bin/env python3
"""Generate garden-manifest.json from vault markdown files.

Walks all .md files, extracts YAML frontmatter, and builds a manifest
with a file/directory tree and metadata map.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

SKIP_DIRS = {'.git', '.obsidian', '.stfolder', '.github'}


def load_gitignore_dirs(repo_root):
    """Parse .gitignore for directory patterns to exclude."""
    gitignore = os.path.join(repo_root, '.gitignore')
    ignored = set()
    if not os.path.exists(gitignore):
        return ignored
    with open(gitignore, 'r') as f:
        for line in f:
            line = line.strip().strip('/')
            if not line or line.startswith('#'):
                continue
            # Treat each non-glob entry as a potential directory name
            if '*' not in line and '?' not in line:
                ignored.add(line)
    return ignored


def parse_frontmatter_and_title(filepath):
    """Extract YAML frontmatter and first H1 title. Returns ({frontmatter}, title|None)."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read(8192)
    except (OSError, UnicodeDecodeError):
        return {}, None

    body = content
    result = {}

    if content.startswith('---'):
        end = content.find('\n---', 3)
        if end != -1:
            block = content[3:end].strip()
            body = content[end + 4:]

            for line in block.split('\n'):
                m = re.match(r'^([A-Za-z0-9_-]+):\s*(.*)', line)
                if not m:
                    continue
                key = m.group(1)
                val = m.group(2).strip().strip("'\"")

                if val.lower() == 'true':
                    result[key] = True
                elif val.lower() == 'false':
                    result[key] = False
                elif val.lower() == 'null' or val == '':
                    result[key] = None
                else:
                    result[key] = val

    # Extract first H1 from body
    title = None
    h1 = re.search(r'^\s*#\s+(.+)$', body, re.MULTILINE)
    if h1:
        title = h1.group(1).strip()

    return result, title


def should_skip(parts):
    """Check if any path component is in the skip set."""
    return any(p in SKIP_DIRS or p.startswith('.') for p in parts)


def main():
    repo_root = sys.argv[1] if len(sys.argv) > 1 else '.'
    repo_root = os.path.abspath(repo_root)

    gitignored = load_gitignore_dirs(repo_root)
    skip_all = SKIP_DIRS | gitignored

    tree = []
    metadata = {}

    for dirpath, dirnames, filenames in os.walk(repo_root):
        # Prune hidden/skipped/gitignored directories
        dirnames[:] = [d for d in dirnames if d not in skip_all and not d.startswith('.')]
        dirnames.sort()

        rel_dir = os.path.relpath(dirpath, repo_root)
        if rel_dir == '.':
            rel_dir = ''

        # Add directory entry (skip root)
        if rel_dir:
            parts = rel_dir.split(os.sep)
            if not should_skip(parts):
                tree.append({'path': rel_dir, 'type': 'dir'})

        # Add files
        for fname in sorted(filenames):
            if fname.startswith('.'):
                continue

            rel_path = os.path.join(rel_dir, fname) if rel_dir else fname
            parts = rel_path.split(os.sep)

            if should_skip(parts):
                continue

            # Only include .md and .base files
            if not (fname.endswith('.md') or fname.endswith('.base')):
                continue

            tree.append({'path': rel_path, 'type': 'file'})

            # Extract frontmatter and title for .md files
            if fname.endswith('.md'):
                full_path = os.path.join(dirpath, fname)
                fm, title = parse_frontmatter_and_title(full_path)
                if title:
                    fm['title'] = title
                if fm:
                    metadata[rel_path] = fm

    manifest = {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'tree': tree,
        'metadata': metadata,
    }

    output_path = os.path.join(repo_root, 'garden-manifest.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    files = sum(1 for e in tree if e['type'] == 'file')
    dirs = sum(1 for e in tree if e['type'] == 'dir')
    published = sum(1 for v in metadata.values() if v.get('published_to_garden') is True)
    print(f'Manifest generated: {files} files, {dirs} dirs, {published} published notes')


if __name__ == '__main__':
    main()
