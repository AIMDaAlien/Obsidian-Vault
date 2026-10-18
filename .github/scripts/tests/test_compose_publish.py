import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from composelib import ComposeError
from composelib.publish import (RunReport, commit_and_push, fast_forward, read_last_counts,
                                run_gate, write_report)

SCRIPTS = Path(__file__).resolve().parent.parent
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "compose"


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout


def init_identity(repo):
    git(repo, "config", "user.name", "Test")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "commit.gpgsign", "false")


def make_origin_and_clone(tmp: Path, with_gate=False):
    """Bare-ish origin (a plain repo accepting pushes) plus a clone with one commit."""
    seed = tmp / "seed"
    seed.mkdir()
    git(seed, "init", "-b", "main")
    init_identity(seed)
    (seed / "README.md").write_text("hello\n")
    if with_gate:
        (seed / ".github/scripts").mkdir(parents=True)
        shutil.copy(SCRIPTS / "privacy-gate.py", seed / ".github/scripts/privacy-gate.py")
    git(seed, "add", "-A")
    git(seed, "commit", "-m", "seed")
    origin = tmp / "origin.git"
    git(tmp, "clone", "--bare", str(seed), str(origin))
    clone = tmp / "clone"
    git(tmp, "clone", str(origin), str(clone))
    init_identity(clone)
    return origin, clone


class TmpCase(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.addCleanup(self._td.cleanup)
        self.tmp = Path(self._td.name)


class FastForward(TmpCase):
    def test_clean_clone_fast_forwards(self):
        origin, clone = make_origin_and_clone(self.tmp)
        other = self.tmp / "other"
        git(self.tmp, "clone", str(origin), str(other))
        init_identity(other)
        (other / "new.md").write_text("x\n")
        git(other, "add", "-A")
        git(other, "commit", "-m", "upstream")
        git(other, "push", "origin", "HEAD:main")
        head = fast_forward(clone)
        self.assertEqual(head, git(other, "rev-parse", "HEAD").strip())
        self.assertTrue((clone / "new.md").exists())

    def test_local_unpushed_commit_fails_diverged(self):
        _, clone = make_origin_and_clone(self.tmp)
        (clone / "local.md").write_text("x\n")
        git(clone, "add", "-A")
        git(clone, "commit", "-m", "local only")
        with self.assertRaises(ComposeError) as cm:
            fast_forward(clone)
        self.assertTrue(str(cm.exception).startswith("remote diverged"))
        self.assertEqual(git(clone, "log", "-1", "--format=%s").strip(), "local only")


class Gate(TmpCase):
    def test_gate_failure_resets_index(self):
        _, clone = make_origin_and_clone(self.tmp, with_gate=True)
        token = "tskey-" + "auth-" + "abcdefghij1234567890"
        (clone / "leak.md").write_text(f"key {token}\n")
        ok, output = run_gate(clone)
        self.assertFalse(ok)
        self.assertIn("leak.md", output)
        self.assertEqual(git(clone, "diff", "--cached", "--name-only").strip(), "")

    def test_gate_pass(self):
        _, clone = make_origin_and_clone(self.tmp, with_gate=True)
        (clone / "ok.md").write_text("fine\n")
        ok, _ = run_gate(clone)
        self.assertTrue(ok)
        self.assertEqual(git(clone, "diff", "--cached", "--name-only").strip(), "ok.md")


class CommitAndPush(TmpCase):
    def test_clean_index_returns_none(self):
        _, clone = make_origin_and_clone(self.tmp)
        self.assertIsNone(commit_and_push(clone, "msg", push=True))

    def test_commit_and_push(self):
        origin, clone = make_origin_and_clone(self.tmp)
        (clone / "a.md").write_text("a\n")
        git(clone, "add", "-A")
        sha = commit_and_push(clone, "msg", push=True)
        self.assertEqual(sha, git(origin, "rev-parse", "main").strip())


class Report(TmpCase):
    def report(self, **kw):
        return RunReport(timestamp="2026-10-18 04:00", status="ok", counts={"m5pro": 3, "bigrig": 3}, **kw)

    def test_write_and_read_counts(self):
        md, js = self.tmp / "r.md", self.tmp / "r.json"
        write_report(md, js, self.report())
        self.assertEqual(read_last_counts(js), {"m5pro": 3, "bigrig": 3})
        self.assertEqual(json.loads(js.read_text())["status"], "ok")

    def test_missing_json_gives_empty_counts(self):
        self.assertEqual(read_last_counts(self.tmp / "none.json"), {})

    def test_markdown_has_status_line(self):
        md = self.tmp / "r.md"
        write_report(md, self.tmp / "r.json", self.report(unresolved=["x.png (missing)"]))
        text = md.read_text(encoding="utf-8")
        self.assertEqual(text.splitlines()[0], "# vault publish 2026-10-18 04:00 — ok")
        self.assertIn("x.png (missing)", text)


class Cli(TmpCase):
    def setUp(self):
        super().setUp()
        self.origin, self.clone = make_origin_and_clone(self.tmp, with_gate=True)
        self.work = self.tmp / "work"
        shutil.copytree(FIXTURE, self.work, ignore=shutil.ignore_patterns("compose.yml"))
        cfg = (FIXTURE / "compose.yml").read_text().replace("published: published", f"published: {self.clone}")
        self.config = self.work / "compose.yml"
        self.config.write_text(cfg)

    def run_cli(self, *extra):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "compose.py"), "--config", str(self.config),
             "--skip-syncthing-check", *extra],
            cwd=self.tmp, capture_output=True, text=True)

    def origin_head(self):
        return git(self.origin, "rev-parse", "main").strip()

    def test_dry_run_leaves_clone_clean_and_prints_stat(self):
        before = self.origin_head()
        proc = self.run_cli("--dry-run")
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertIn("files changed", proc.stdout)
        self.assertEqual(git(self.clone, "status", "--porcelain").strip(), "")
        self.assertEqual(self.origin_head(), before)
        self.assertIn("— dry-run", (self.work / "last-run.md").read_text(encoding="utf-8"))

    def test_no_push_commits_locally(self):
        before = self.origin_head()
        proc = self.run_cli("--no-push")
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertTrue(git(self.clone, "log", "-1", "--format=%s").startswith("vault publish:"))
        self.assertEqual(self.origin_head(), before)

    def test_push_then_second_run_is_noop(self):
        self.assertEqual(self.run_cli().returncode, 0)
        self.assertNotEqual(self.origin_head(), "")
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertIn("— no-op", (self.work / "last-run.md").read_text(encoding="utf-8"))

    def test_collision_exits_1_and_reports(self):
        (self.work / "bigrig" / "Index.md").write_text("# clash\n")
        proc = self.run_cli("--no-push")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("collision:", (self.work / "last-run.md").read_text(encoding="utf-8"))

    def test_missing_api_key_fails(self):
        proc = subprocess.run([sys.executable, str(SCRIPTS / "compose.py"), "--config", str(self.config)],
                              cwd=self.tmp, capture_output=True, text=True,
                              env={"PATH": "/usr/bin:/bin"})
        self.assertEqual(proc.returncode, 1)
        self.assertIn("syncthing api key missing", (self.work / "last-run.md").read_text(encoding="utf-8"))

    def test_bad_arguments_exit_2(self):
        proc = subprocess.run([sys.executable, str(SCRIPTS / "compose.py")], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)

    def test_commit_message_counts(self):
        self.run_cli("--no-push")
        subject = git(self.clone, "log", "-1", "--format=%s")
        self.assertIn("(m5pro 3 notes, bigrig 3 notes)", subject)

    def test_curation_copied_and_applied(self):
        curation = self.work / "curation.yml"
        curation.write_text('- path: "01 Projects/Penthouse/Penthouse Remake.md"\n'
                            '  featured: 2\n  summary: "A remake."\n')
        proc = self.run_cli("--no-push", "--curation", str(curation))
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertTrue((self.clone / "curation.yml").is_file())
        note = (self.clone / "01 Projects/Penthouse/Penthouse Remake.md").read_text(encoding="utf-8")
        self.assertIn("featured: 2", note)
        self.assertIn("summary:", note)


if __name__ == "__main__":
    unittest.main()
