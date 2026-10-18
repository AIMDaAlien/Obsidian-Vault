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
        self.assertIn("unpushed local commit", str(cm.exception))
        self.assertIn("ahead of origin/main", str(cm.exception))
        self.assertEqual(git(clone, "log", "-1", "--format=%s").strip(), "local only")

    def test_true_divergence_says_remote_diverged(self):
        origin, clone = make_origin_and_clone(self.tmp)
        other = self.tmp / "other"
        git(self.tmp, "clone", str(origin), str(other))
        init_identity(other)
        (other / "up.md").write_text("x\n")
        git(other, "add", "-A")
        git(other, "commit", "-m", "upstream")
        git(other, "push", "origin", "HEAD:main")
        (clone / "local.md").write_text("x\n")
        git(clone, "add", "-A")
        git(clone, "commit", "-m", "local only")
        with self.assertRaises(ComposeError) as cm:
            fast_forward(clone)
        self.assertTrue(str(cm.exception).startswith("remote diverged"))


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


    def test_push_failure_keeps_commit_and_reason(self):
        from composelib.publish import PushError
        origin, clone = make_origin_and_clone(self.tmp)
        git(clone, "remote", "set-url", "origin", str(self.tmp / "nowhere.git"))
        (clone / "a.md").write_text("a\n")
        git(clone, "add", "-A")
        with self.assertRaises(PushError) as cm:
            commit_and_push(clone, "msg", push=True)
        self.assertTrue(str(cm.exception).startswith("push failed:"))
        self.assertEqual(cm.exception.commit, git(clone, "rev-parse", "HEAD").strip())


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

    def last_md(self):
        return (self.work / "last-run.md").read_text(encoding="utf-8")

    def test_malformed_curation_yaml_fails_with_report(self):
        (self.work / "curation.yml").write_text("- path: [unclosed\n")
        proc = self.run_cli("--no-push")
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(self.last_md().splitlines()[0].endswith("— failed"))

    def test_explicit_missing_curation_fails(self):
        missing = self.work / "nope.yml"
        proc = self.run_cli("--no-push", "--curation", str(missing))
        self.assertEqual(proc.returncode, 1)
        self.assertIn(f"curation file missing: {missing}", self.last_md())

    def test_default_curation_absent_is_skipped(self):
        proc = self.run_cli("--no-push")
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertFalse((self.clone / "curation.yml").exists())

    def test_mac_note_untouched_bigrig_notes_get_machine(self):
        proc = self.run_cli("--no-push")
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        src = (self.work / "m5pro" / "Index.md").read_text(encoding="utf-8")
        pub = (self.clone / "Index.md").read_text(encoding="utf-8")
        self.assertNotIn("machine:", pub.split("---")[1])
        self.assertEqual(pub.split("---")[1], src.split("---")[1])
        remake = (self.clone / "01 Projects/Penthouse/Penthouse Remake.md").read_text(encoding="utf-8")
        self.assertIn("machine: bigrig", remake)

    def test_curation_rank_clash_with_mac_frontmatter_fails(self):
        curation = self.work / "curation.yml"
        curation.write_text('- path: "01 Projects/Penthouse/Penthouse Remake.md"\n  featured: 1\n')
        proc = self.run_cli("--no-push")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("rank 1 already used by Index.md", self.last_md())

    def test_gate_hit_fails_and_leaves_index_and_origin_clean(self):
        token = "tskey-" + "auth-" + "abcdefghij1234567890"
        (self.work / "bigrig" / "Leak.md").write_text(f"# Leak\n\n{token}\n")
        before = self.origin_head()
        proc = self.run_cli("--no-push")
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(self.last_md().splitlines()[0].endswith("— failed"))
        subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=self.clone, check=True)
        self.assertEqual(self.origin_head(), before)

    def test_stale_curation_removed_when_curation_goes_away(self):
        curation = self.work / "curation.yml"
        curation.write_text('- path: "01 Projects/Penthouse/Penthouse Remake.md"\n  featured: 2\n')
        self.assertEqual(self.run_cli().returncode, 0)
        self.assertTrue((self.clone / "curation.yml").is_file())
        curation.unlink()
        self.assertEqual(self.run_cli().returncode, 0)
        self.assertFalse((self.clone / "curation.yml").exists())
        self.assertIn("curation.yml", git(self.clone, "show", "--name-status", "--format=", "HEAD"))

    def counts(self):
        return json.loads((self.work / "last-run.json").read_text())["counts"]

    def test_dry_run_preserves_counts(self):
        self.assertEqual(self.run_cli().returncode, 0)
        self.assertEqual(self.counts(), {"m5pro": 3, "bigrig": 3})
        (self.work / "bigrig" / "Extra.md").write_text("# Extra\n")
        self.assertEqual(self.run_cli("--dry-run").returncode, 0)
        self.assertEqual(self.counts(), {"m5pro": 3, "bigrig": 3})

    def test_early_failure_preserves_counts(self):
        self.assertEqual(self.run_cli().returncode, 0)
        proc = subprocess.run([sys.executable, str(SCRIPTS / "compose.py"), "--config",
                               str(self.work / "missing.yml"), "--report-dir", str(self.work),
                               "--skip-syncthing-check"], cwd=self.tmp, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(self.last_md().splitlines()[0].endswith("— failed"))
        self.assertEqual(self.counts(), {"m5pro": 3, "bigrig": 3})

    def test_corrupt_last_run_json_fails_and_is_preserved(self):
        path = self.work / "last-run.json"
        path.write_bytes(b"{not json")
        proc = self.run_cli("--no-push")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("last-run.json unreadable:", self.last_md())
        self.assertEqual(path.read_bytes(), b"{not json")

    def test_first_run_failure_writes_no_counts(self):
        (self.work / "bigrig" / "Index.md").write_text("# clash\n")
        self.assertEqual(self.run_cli("--no-push").returncode, 1)
        self.assertEqual(self.counts(), {})

    def test_missing_terms_file_fails_before_gate(self):
        token = "tskey-" + "auth-" + "abcdefghij1234567890"
        (self.work / "bigrig" / "Leak.md").write_text(f"# Leak\n\n{token}\n")
        before_origin, before_clone = self.origin_head(), git(self.clone, "rev-parse", "HEAD")
        missing = self.work / "no-terms"
        proc = self.run_cli("--require-terms", str(missing))
        self.assertEqual(proc.returncode, 1)
        md = self.last_md()
        self.assertTrue(md.splitlines()[0].endswith("— failed"))
        self.assertIn(f"privacy terms file missing: {missing}", md)
        self.assertNotIn("privacy gate failed", md)
        self.assertEqual(self.origin_head(), before_origin)
        self.assertEqual(git(self.clone, "rev-parse", "HEAD"), before_clone)
        self.assertEqual(git(self.clone, "status", "--porcelain").strip(), "")

    def test_empty_terms_file_fails(self):
        terms = self.work / "terms"
        terms.write_text("# only a comment\n\n")
        proc = self.run_cli("--no-push", "--require-terms", str(terms))
        self.assertEqual(proc.returncode, 1)
        self.assertIn(f"privacy terms file missing: {terms}", self.last_md())

    def test_present_terms_file_runs(self):
        terms = self.work / "terms"
        terms.write_text("some-unused-phrase-xyz\n")
        proc = self.run_cli("--no-push", "--require-terms", str(terms))
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)

    def test_bad_featured_in_github_fixture_does_not_fail_run(self):
        fixture = self.clone / ".github/scripts/tests/fixtures/x.md"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("---\nfeatured: yes\n---\n# X\n")
        proc = self.run_cli("--no-push")
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)

    def test_push_failure_reports_commit_and_reason(self):
        git(self.clone, "remote", "set-url", "--push", "origin", str(self.tmp / "nowhere.git"))
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("push failed:", self.last_md())
        data = json.loads((self.work / "last-run.json").read_text())
        self.assertEqual(data["commit"], git(self.clone, "rev-parse", "HEAD").strip())


if __name__ == "__main__":
    unittest.main()
