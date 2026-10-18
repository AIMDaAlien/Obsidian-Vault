#!/usr/bin/env python3
"""Privacy gate: fail when git-tracked text files contain secrets or identifiers.

Scans every blob in the git index (what would be committed, not the working
tree), including symlink targets, and skips only binary blobs (a NUL byte in
the first 8 KB). It looks for private IPs, public IPs,
MAC addresses, Tailscale/DuckDNS hosts, phone numbers, credentials, home
directory paths and any phrase listed in ~/.vault-privacy-terms. Lines inside
fenced code blocks are scanned too. New image files are listed for manual
review but never fail the run.

Runs in GitHub Actions, in the local sync script and as a git pre-commit hook.
Python 3.10+, standard library only.

Exit 0: clean. Exit 1: one "path:line: pattern" per hit, then a summary line.
"""
import argparse
import os
import re
import subprocess
import sys

TERMS_PATH = os.path.expanduser('~/.vault-privacy-terms')
IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')
# The gate's test fixtures and test cases would trip it; skipped by prefix.
SELF_PATHS = ('.github/scripts/tests/fixtures/gate/', '.github/scripts/tests/test_privacy_gate.py')
BINARY_SNIFF = 8192  # a NUL byte in this many leading bytes marks a binary blob
GITLINK_MODE = '160000'  # submodule entry: no blob to read

IPV4 = re.compile(r'(?<!\d)(?<!\d\.)((?:\d{1,3}\.){3}\d{1,3})(?!\d)(?!\.\d)')
# A version word directly before the value ("LGUP 1.16.0.3", "version: v2.1.0.5").
VERSION_BEFORE = re.compile(
    r'\b(?:firmware|version|bios|build|release|rev|lgup|kdz|agesa)\b[:\s]{0,12}v?$', re.I)
IP_ALLOWLIST = frozenset((
    '127.0.0.1', '0.0.0.0', '1.1.1.1', '1.0.0.1', '8.8.8.8', '8.8.4.4',
    '9.9.9.9', '149.112.112.112', '208.67.222.222', '208.67.220.220',
    '104.21.9.162', '172.67.160.73', '216.198.79.1', '192.168.1.1',
    '10.6.0.1', '172.17.0.1',
))
PLACEHOLDER_USERS = frozenset(('username', 'you', 'user', 'yourname'))

PHONE = re.compile(r'(?<![\d.-])(?:\+?1[-. ]?)?(?:\((\d{3})\)\s?|(\d{3})[-.\s])(\d{3})[-.\s](\d{4})(?![\d-])')
CODE_SPAN = re.compile(r'`[^`\n]*`')
FENCE = re.compile(r'\s*(`{3,}|~{3,})')
PHONE_BARE = re.compile(r'\b(\d{3})(\d{3})(\d{4})\b')  # ten digits, no separators
# macOS home paths (also inside file:// URLs) and Windows profile paths, with
# single or escaped double backslashes and any letter case for the Windows form.
HOME_PATH = re.compile(r'(?<![\w\\])(?:/Users/|(?i:c:\\{1,2}users\\{1,2}))([A-Za-z]+)')
HEX_PAIR = re.compile(r'[0-9A-Fa-f]{2}')
MAC = re.compile(r'(?=(?<![0-9A-Fa-f])((?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})(?![0-9A-Fa-f]))')
PRIVATE_KEY = re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY(?: BLOCK)?-----')

# Regex patterns in report order. lan_ip and public_ip are handled by IPV4.
PATTERNS = [
    ('lan_ip', IPV4),
    ('public_ip', IPV4),
    ('mac', MAC),
    ('tailscale_auth', re.compile(r'login\.tailscale\.com/a/')),
    ('duckdns', re.compile(r'[A-Za-z0-9.-]+\.duckdns\.org(?![A-Za-z0-9-])', re.I)),
    ('ts_net', re.compile(r'[A-Za-z0-9.-]+\.ts\.net(?![A-Za-z0-9-])', re.I)),
    ('phone', PHONE),
    ('private_key', PRIVATE_KEY),
    ('tskey', re.compile(r'tskey-[A-Za-z0-9-]+')),
    ('github_token', re.compile(r'gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{20,}')),
    ('aws_key', re.compile(r'AKIA[0-9A-Z]{16}')),
    ('discord_webhook', re.compile(r'discord(?:app)?\.com/api/webhooks/')),
    ('home_path', HOME_PATH),
    ('ssh' 'pass', re.compile(r'\bssh' r'pass\b')),  # split so this file scans clean
    ('env_unraid', re.compile(r'\.env\.unraid')),
    ('private_deployment', re.compile(r'\.chatgpt\.site\b')),
    ('extra_term', None),  # built per run from load_extra_terms()
]


def parse_ipv4(s):
    """Return a 4-tuple of ints, or None if s is not a valid dotted quad."""
    parts = s.split('.')
    if len(parts) != 4:
        return None
    for p in parts:
        if not p.isdigit() or int(p) > 255 or (len(p) > 1 and p[0] == '0'):
            return None
    return tuple(int(p) for p in parts)


def is_rfc1918(t):
    return t[0] == 10 or (t[0] == 172 and 16 <= t[1] <= 31) or (t[0] == 192 and t[1] == 168)


CIDR_SUFFIX = re.compile(r'/(\d+)')


def is_network_cidr(t, line, end):
    """True if `/N` follows the address at `end` and t is a network for /N.

    Only 0 <= N <= 32 with all host bits zero counts. A host address with a
    mask, or an address followed by a numeric URL path segment, is still an
    address and is reported. The test suite has concrete examples.
    """
    m = CIDR_SUFFIX.match(line, end)
    if not m or int(m.group(1)) > 32:
        return False
    host_bits = 32 - int(m.group(1))
    value = (t[0] << 24) | (t[1] << 16) | (t[2] << 8) | t[3]
    return value & ((1 << host_bits) - 1) == 0


def is_allowlisted(value, before):
    """True if the IPv4 `value` is expected, so is not a hit.

    `before` is the line text preceding the address. A version word directly
    before it (at most 12 characters of colons, spaces and one optional "v"
    between) marks a version string, never for RFC1918 addresses.
    """
    t = parse_ipv4(value)
    if t is None:
        return True
    if not is_rfc1918(t) and VERSION_BEFORE.search(before[-40:]):
        return True
    return value in IP_ALLOWLIST or t[3] == 0 or t[0] == 127 or t[0] == 0


def _is_doc_phone(area, exchange):
    return '555' in (area, exchange)  # documentation numbers


def _standalone_pair(line, i):
    """True if line[i:i+2] is a hex pair not glued to a preceding word character."""
    return (i >= 0 and HEX_PAIR.fullmatch(line[i:i + 2]) is not None
            and (i == 0 or not line[i - 1].isalnum()))


def _is_mac(line, m):
    """A 6-pair run that is not part of a longer hex-pair chain (e.g. a WWN)."""
    start, end = m.start(1), m.end(1)
    if start >= 3 and line[start - 1] in ':-' and _standalone_pair(line, start - 3):
        return False
    after = line[end + 1:end + 4]
    if line[end:end + 1] in (':', '-') and HEX_PAIR.fullmatch(after[:2] or '') \
            and not after[2:3].isalnum():
        return False
    return True


def _phrase_regex(term):
    body = r'\s+'.join(re.escape(w) for w in term.split())
    tail = r'(?!\w)' if term[-1:].isalnum() else ''
    return re.compile(r'(?<!\w)' + body + tail, re.I)


def _mask_code_spans(line):
    """Blank out single-backtick code spans on one line (same length)."""
    return CODE_SPAN.sub(lambda m: ' ' * len(m.group(0)), line)


def _line_kinds(line, extra_res, in_fence=False):
    kinds = set()
    for m in IPV4.finditer(line):
        value = m.group(1)
        t = parse_ipv4(value)
        if t is not None and is_network_cidr(t, line, m.end(1)):
            continue  # network prefix such as 192.168.0.0/24
        if is_allowlisted(value, line[:m.start(1)]):
            continue
        kinds.add('lan_ip' if is_rfc1918(parse_ipv4(value)) else 'public_ip')
    for name, rx in PATTERNS:
        if rx is None or rx is IPV4:
            continue
        for m in rx.finditer(line):
            if name == 'phone' and _is_doc_phone(m.group(1) or m.group(2), m.group(3)):
                continue
            if name == 'home_path' and m.group(1).lower() in PLACEHOLDER_USERS:
                continue
            if name == 'mac' and not _is_mac(line, m):
                continue
            kinds.add(name)
            break
    # The bare 10-digit form ignores code spans and fenced blocks (counters,
    # sysctl values); every other pattern scans the full line.
    bare = '' if in_fence else _mask_code_spans(line)
    if 'phone' not in kinds and any(not _is_doc_phone(m.group(1), m.group(2))
                                    for m in PHONE_BARE.finditer(bare)):
        kinds.add('phone')
    if any(rx.search(line) for rx in extra_res):
        kinds.add('extra_term')
    return kinds


def scan_text(text, path, extra_terms):
    """Return [(path, 1-based line, pattern name)], one per pattern per line."""
    extra_res = [_phrase_regex(t) for t in extra_terms if t.strip()]
    order = [name for name, _ in PATTERNS]
    hits = []
    fence = None  # opening fence marker while inside a fenced block
    for n, line in enumerate(text.splitlines(), 1):
        fm = FENCE.match(line)
        in_fence = fence is not None
        if fm:
            marker = fm.group(1)
            if fence is None:
                fence, in_fence = marker, True
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
        for kind in sorted(_line_kinds(line, extra_res, in_fence), key=order.index):
            hits.append((path, n, kind))
    return hits


class GitError(Exception):
    pass


def _git(root, *args, check=True):
    result = subprocess.run(['git', '-C', root, *args], capture_output=True,
                            text=True, encoding='utf-8', errors='replace')
    if check and result.returncode != 0:
        raise GitError(result.stderr.strip() or 'git %s failed' % args[0])
    return result


def index_blobs(repo_root):
    """[(path, bytes)] for every index entry outside SELF_PATHS, sorted by path.

    Reads blobs from the index, so a symlink (mode 120000) yields its target
    text. Binary blobs are included here and skipped by the caller.
    """
    ls = subprocess.run(['git', '-C', repo_root, 'ls-files', '-s', '-z'], capture_output=True)
    if ls.returncode != 0:
        raise GitError(ls.stderr.decode('utf-8', 'replace').strip() or 'git ls-files failed')
    entries = {}
    for rec in ls.stdout.split(b'\0'):
        if not rec:
            continue
        meta, path = rec.split(b'\t', 1)
        mode, sha, _stage = meta.decode().split()
        path = path.decode('utf-8', 'replace')
        if mode == GITLINK_MODE or path.startswith(SELF_PATHS):
            continue
        entries[path] = sha
    if not entries:
        return []
    paths = sorted(entries)
    cat = subprocess.run(['git', '-C', repo_root, 'cat-file', '--batch'],
                         input=b''.join(entries[p].encode() + b'\n' for p in paths),
                         capture_output=True)
    if cat.returncode != 0:
        raise GitError(cat.stderr.decode('utf-8', 'replace').strip() or 'git cat-file failed')
    out, pos, blobs = cat.stdout, 0, []
    for p in paths:
        nl = out.index(b'\n', pos)
        header = out[pos:nl].split()
        if len(header) != 3:
            raise GitError('cannot read blob for %s' % p)
        size = int(header[2])
        blobs.append((p, out[nl + 1:nl + 1 + size]))
        pos = nl + 1 + size + 1
    return blobs


def is_binary(data):
    return b'\0' in data[:BINARY_SNIFF]


def _valid_ref(repo_root, ref):
    if not ref or set(ref) == {'0'}:
        return False
    return _git(repo_root, 'rev-parse', '--verify', '--quiet', ref + '^{commit}', check=False).returncode == 0


def new_images(repo_root, base_ref):
    """Image paths added since base_ref, or staged/untracked when no valid ref."""
    if _valid_ref(repo_root, base_ref):
        out = _git(repo_root, 'diff', '--name-only', '--diff-filter=A', base_ref, 'HEAD').stdout
    else:
        out = (_git(repo_root, 'diff', '--cached', '--name-only', '--diff-filter=A').stdout
               + _git(repo_root, 'ls-files', '--others', '--exclude-standard').stdout)
    return sorted({p for p in out.splitlines() if p.lower().endswith(IMAGE_EXTS)})


def load_extra_terms(path=None):
    """Non-blank, non-comment lines of the private terms file; [] when it is absent."""
    try:
        with open(path or TERMS_PATH, encoding='utf-8', errors='replace') as f:
            lines = [line.strip() for line in f]
        return [t for t in lines if t and not t.startswith('#')]
    except OSError:
        return []


def main(argv=None):
    ap = argparse.ArgumentParser(description='Fail on secrets or identifiers in tracked files.')
    ap.add_argument('--root', help='repository root (default: git toplevel of cwd)')
    ap.add_argument('--base-ref', help='report images added since this ref')
    args = ap.parse_args(argv)
    try:
        root = args.root or _git('.', 'rev-parse', '--show-toplevel').stdout.strip()
        blobs = [(p, d) for p, d in index_blobs(root) if not is_binary(d)]
        images = new_images(root, args.base_ref)
    except GitError as e:
        print('privacy gate: git error: %s' % e, file=sys.stderr)
        return 2
    if not blobs:
        print('privacy gate: no tracked text files to scan', file=sys.stderr)
        return 2
    if not os.path.exists(TERMS_PATH):
        print('privacy gate: note: no ~/.vault-privacy-terms, extra terms not checked',
              file=sys.stderr)
    terms = load_extra_terms()
    hits = []
    for rel, data in blobs:
        hits.extend(scan_text(data.decode('utf-8', errors='replace'), rel, terms))
    for path in images:
        print('review image: ' + path)
    if hits:
        for path, line, name in sorted(hits, key=lambda h: (h[0], h[1])):
            print('%s:%d: %s' % (path, line, name))
        print('privacy gate: %d hits' % len(hits))
        return 1
    print('privacy gate: clean, %d files' % len(blobs))
    return 0


if __name__ == '__main__':
    sys.exit(main())
