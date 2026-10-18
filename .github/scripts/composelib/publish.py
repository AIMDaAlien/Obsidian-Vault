"""Git, privacy gate, Syncthing, report and notification helpers for a compose run."""
import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import ComposeError

NOTIFY_SCRIPT = Path("/usr/local/emhttp/webGui/scripts/notify")
GATE_SCRIPT = ".github/scripts/privacy-gate.py"


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise ComposeError(f"git {' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return proc


class PushError(ComposeError):
    """The commit exists locally but could not be pushed."""

    def __init__(self, message: str, commit: str):
        super().__init__(message)
        self.commit = commit


BUSY_STATES = {"scanning", "syncing", "sync-preparing", "sync-waiting", "scan-waiting",
               "cleaning", "clean-waiting"}


def _folder_state(base: str, api_key: str, folder: str) -> str:
    """The folder's Syncthing state; raises on HTTP, network or JSON trouble."""
    req = urllib.request.Request(f"{base}/rest/db/status?folder={urllib.parse.quote(folder)}",
                                 headers={"X-API-Key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        exc.close()
        raise
    state = data.get("state") if isinstance(data, dict) else None
    if not isinstance(state, str) or not state:
        raise ValueError("no state in response")
    return state


def syncthing_idle(api: str, api_key: str, folder_ids: list[str]) -> tuple[str, str]:
    """("idle" | "busy" | "error", detail) over every folder; an error outranks busy.

    Busy means a folder is scanning or syncing; idle means all are idle. Any other
    state, or any HTTP, network or JSON failure, is an error.
    """
    base = api if "://" in api else f"http://{api}"
    errors, busy = [], []
    for folder in folder_ids:
        try:
            state = _folder_state(base, api_key, folder)
        except Exception as exc:  # HTTP, network, timeout, bad JSON
            errors.append(f"syncthing: {folder}: {type(exc).__name__}: {exc}")
            continue
        if state in BUSY_STATES:
            busy.append(f"syncthing folder {folder} is {state}")
        elif state != "idle":
            errors.append(f"syncthing: {folder}: {state}")
    if errors:
        return "error", "\n".join(errors)
    if busy:
        return "busy", "; ".join(busy)
    return "idle", "idle"


def fast_forward(repo: Path) -> str:
    """Move the clone to origin/main, refusing when local HEAD has unpushed work."""
    _git(repo, "fetch", "origin", "main")
    if _git(repo, "merge-base", "--is-ancestor", "HEAD", "origin/main", check=False).returncode != 0:
        if _git(repo, "merge-base", "--is-ancestor", "origin/main", "HEAD", check=False).returncode == 0:
            short = _git(repo, "rev-parse", "--short", "HEAD").stdout.strip()
            raise ComposeError(f"unpushed local commit {short} is ahead of origin/main; "
                               "push it or reset the clone")
        raise ComposeError("remote diverged: local HEAD is not an ancestor of origin/main")
    _git(repo, "reset", "--hard", "origin/main")
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def run_gate(repo: Path) -> tuple[bool, str]:
    """Stage everything and run the privacy gate; on failure unstage and return its output."""
    _git(repo, "add", "-A")
    proc = subprocess.run([sys.executable, GATE_SCRIPT], cwd=repo, capture_output=True, text=True)
    output = (proc.stdout + proc.stderr).strip()
    if proc.returncode != 0:
        _git(repo, "reset")
        return False, output
    return True, output


def commit_and_push(repo: Path, message: str, push: bool) -> str | None:
    """Commit the staged changes (and push to main); None when nothing is staged."""
    if _git(repo, "diff", "--cached", "--quiet", check=False).returncode == 0:
        return None
    _git(repo, "commit", "-m", message)
    commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    if push:
        proc = _git(repo, "push", "origin", "HEAD:main", check=False)
        if proc.returncode != 0:
            first = (proc.stderr.strip() or proc.stdout.strip()).splitlines()[:1]
            raise PushError(f"push failed: {first[0] if first else 'unknown error'}", commit)
    return commit


@dataclass
class RunReport:
    timestamp: str
    status: str  # ok, no-op, busy, dry-run, failed
    counts: dict[str, int] = field(default_factory=dict)
    added: int = 0
    changed: int = 0
    removed: int = 0
    unresolved: list[str] = field(default_factory=list)
    unwrapped: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    gate: str = ""
    commit: str | None = None
    duration_s: float = 0.0
    reason: str = ""


def _bullets(items: list[str]) -> list[str]:
    return [f"- {i}" for i in items] or ["- none"]


def write_report(md_path: Path, json_path: Path | None, report: RunReport) -> None:
    lines = [
        f"# vault publish {report.timestamp} — {report.status}",
        "",
        f"- reason: {report.reason or '-'}",
        f"- commit: {report.commit or '-'}",
        f"- counts: {', '.join(f'{k} {v}' for k, v in report.counts.items()) or '-'}",
        f"- files: {report.added} added, {report.changed} changed, {report.removed} removed",
        f"- duration: {report.duration_s:.1f}s",
        f"- gate: {report.gate or '-'}",
        "",
        "## Unresolved embeds", *_bullets(report.unresolved), "",
        "## Unwrapped links", *_bullets(report.unwrapped), "",
        "## Skipped protected", *_bullets(report.skipped), "",
    ]
    Path(md_path).write_text("\n".join(lines), encoding="utf-8")
    if json_path is None:
        return
    Path(json_path).write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")


def read_last_counts(json_path: Path) -> dict[str, int]:
    path = Path(json_path)
    if not path.is_file():
        return {}
    return dict(json.loads(path.read_text(encoding="utf-8")).get("counts", {}))


def notify(reason: str) -> None:
    """Raise an Unraid warning when available, else log to stderr. Never raises."""
    try:
        if NOTIFY_SCRIPT.exists():
            subprocess.run([str(NOTIFY_SCRIPT), "-i", "warning", "-s", "vault publish", "-d", reason],
                           check=False, timeout=30)
        else:
            print(f"notify: {reason}", file=sys.stderr)
    except Exception as exc:
        print(f"notify failed: {exc}", file=sys.stderr)
