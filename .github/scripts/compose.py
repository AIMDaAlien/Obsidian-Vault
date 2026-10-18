#!/usr/bin/env python3
"""Compose the published vault from its source vaults and push it (spec 5.2)."""
import argparse
import os
import shutil
import sys
import time
from datetime import date, datetime
from pathlib import Path

from composelib import ComposeError
from composelib.config import load_config
from composelib.links import build_index, resolve_bare_embeds, unwrap_excluded_links
from composelib.notes import (apply_curation, frontmatter_ranks, load_curation,
                              normalize_note, rank_errors, validate_curation)
from composelib.publish import (RunReport, _git, commit_and_push, fast_forward, notify,
                                read_last_counts, run_gate, syncthing_idle, write_report)
from composelib.tree import apply_tree, count_notes, guard_sources, plan_tree, skipped_protected


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--no-push", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-syncthing-check", action="store_true")
    p.add_argument("--curation", type=Path)
    p.add_argument("--report-dir", type=Path)
    return p.parse_args(argv)


def _rewrite(root: Path, rel: str, fn) -> None:
    path = root / rel
    path.write_text(fn(path.read_text(encoding="utf-8")), encoding="utf-8", newline="")


def _compose(args, cfg, report: RunReport, last_counts: dict[str, int]) -> None:
    repo, root = cfg.published, cfg.published
    guard_sources(cfg, last_counts)
    fast_forward(repo)
    plan = plan_tree(cfg)
    report.skipped = skipped_protected(cfg)
    stats = apply_tree(plan, cfg)
    report.added, report.changed, report.removed = stats.added, stats.changed, stats.removed
    machines = {s.name: s.machine for s in cfg.sources}
    mac_paths = {rel for rel, (name, _) in plan.items() if machines[name] == "mac"}
    for rel, (name, src) in plan.items():
        if rel.endswith(".md") and machines[name] != "mac":
            created = date.fromtimestamp(src.stat().st_mtime).isoformat()
            _rewrite(root, rel, lambda t: normalize_note(t, machines[name], created))
    curation = args.curation or args.config.parent / "curation.yml"
    entries = load_curation(curation) if curation.is_file() else []
    errors = rank_errors(root) + validate_curation(entries, root, frontmatter_ranks(root, mac_paths))
    if errors:
        raise ComposeError("curation invalid:\n" + "\n".join(errors))
    for entry in entries:
        _rewrite(root, entry.path, lambda t: apply_curation(t, entry))
    index = build_index(root)
    for rel in plan:
        if not rel.endswith(".md"):
            continue

        def fix(text):
            text, bad = resolve_bare_embeds(text, index, cfg.image_ext)
            text, dead = unwrap_excluded_links(text, index, cfg.exclude_ext, cfg.image_ext)
            report.unresolved += [f"{rel}: {b}" for b in bad]
            report.unwrapped += [f"{rel}: {d}" for d in dead]
            return text
        _rewrite(root, rel, fix)
    if entries:
        shutil.copy2(curation, root / "curation.yml")
    ok, report.gate = run_gate(repo)
    if not ok:
        raise ComposeError("privacy gate failed:\n" + report.gate)
    if args.dry_run:
        print(_git(repo, "diff", "--cached", "--stat").stdout)
        _git(repo, "reset", "--hard", "HEAD")
        _git(repo, "clean", "-fd")
        report.status = "dry-run"
        return
    names = ", ".join(f"{s.name} {report.counts[s.name]} notes" for s in cfg.sources)
    message = f"vault publish: {datetime.now():%Y-%m-%d %H:%M} ({names})"
    report.commit = commit_and_push(repo, message, push=not args.no_push)
    report.status = "ok" if report.commit else "no-op"


def run(args) -> int:
    start = time.monotonic()
    report = RunReport(timestamp=f"{datetime.now():%Y-%m-%d %H:%M}", status="failed")
    report_dir = args.report_dir or args.config.parent
    md_path, json_path = report_dir / "last-run.md", report_dir / "last-run.json"
    code, last_counts = 0, {}
    try:
        cfg = load_config(args.config)
        last_counts = read_last_counts(json_path)
        report.counts = {s.name: count_notes(s.path, cfg.exclude_dirs) if s.path.is_dir() else 0
                         for s in cfg.sources}
        busy = None
        if not args.skip_syncthing_check:
            key = os.environ.get("SYNCTHING_API_KEY")
            if not key:
                raise ComposeError("syncthing api key missing")
            idle, why = syncthing_idle(cfg.syncthing_api, key, [s.syncthing_folder for s in cfg.sources])
            busy = None if idle else why
        if busy:
            report.status, report.reason, report.counts = "busy", busy, last_counts
        else:
            _compose(args, cfg, report, last_counts)
    except ComposeError as exc:
        report.status, report.reason, code = "failed", str(exc), 1
        report.counts = last_counts or report.counts
        notify(str(exc).splitlines()[0])
    report.duration_s = time.monotonic() - start
    report_dir.mkdir(parents=True, exist_ok=True)
    write_report(md_path, json_path, report)
    print(f"vault publish: {report.status} {report.reason}".rstrip())
    return code


def main() -> int:
    return run(parse_args())


if __name__ == "__main__":
    sys.exit(main())
