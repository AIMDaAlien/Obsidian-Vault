import dataclasses
import shutil
import tempfile
import unittest
from pathlib import Path

from composelib import ComposeError
from composelib.config import load_config
from composelib.tree import TreeStats, apply_tree, count_notes, guard_sources, plan_tree, skipped_protected

FIX = Path(__file__).parent / "fixtures" / "compose"


class TempCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def fixture_copy(self):
        """Copy the fixture vaults to a temp dir and return a Config over them.

        The repo's .gitignore ignores _private/ and .obsidian/, so those
        fixture entries cannot be committed; they are created here instead.
        """
        shutil.copytree(FIX, self.tmp / "fx")
        m5 = self.tmp / "fx" / "m5pro"
        (m5 / "_private").mkdir()
        (m5 / "_private" / "Secret.md").write_text("# Secret\n")
        (m5 / ".obsidian").mkdir()
        (m5 / ".obsidian" / "app.json").write_text("{}\n")
        return load_config(self.tmp / "fx" / "compose.yml")


class LoadConfig(unittest.TestCase):
    def test_loads_sources_and_lists(self):
        cfg = load_config(FIX / "compose.yml")
        self.assertEqual([s.name for s in cfg.sources], ["m5pro", "bigrig"])
        self.assertEqual(cfg.sources[1].path_map, {"01 Projects/The Penthouse/": "01 Projects/Penthouse/"})
        self.assertIn("curation.yml", cfg.protected)
        self.assertEqual(cfg.exclude_ext[0], "json")
        self.assertEqual(cfg.sources[0].syncthing_folder, "aaa")
        self.assertEqual(cfg.sources[1].path, FIX / "bigrig")
        self.assertEqual(cfg.published, FIX / "published")


class PlanTree(TempCase):
    def test_mac_note_keeps_path_and_private_is_dropped(self):
        plan = plan_tree(self.fixture_copy())
        self.assertIn("Index.md", plan)
        self.assertEqual(plan["Index.md"][0], "m5pro")
        self.assertFalse([k for k in plan if k.startswith("_private/")])
        self.assertFalse([k for k in plan if ".obsidian/" in k])

    def test_bigrig_path_map_applied(self):
        plan = plan_tree(load_config(FIX / "compose.yml"))
        src, path = plan["01 Projects/Penthouse/Penthouse Remake.md"]
        self.assertEqual(src, "bigrig")
        self.assertEqual(path, FIX / "bigrig" / "01 Projects" / "The Penthouse" / "Penthouse Remake.md")

    def test_only_embedded_images_copied_from_attachments(self):
        plan = plan_tree(load_config(FIX / "compose.yml"))
        self.assertIn("_attachments/run1/lcb60-pareto.png", plan)
        self.assertIn("_attachments/run2/remake.png", plan)
        self.assertNotIn("_attachments/run1/unused.png", plan)
        self.assertNotIn("_attachments/run1/results.json", plan)

    def test_inbox_and_excluded_ext_never_copied(self):
        plan = plan_tree(load_config(FIX / "compose.yml"))
        self.assertFalse([k for k in plan if k.startswith("_inbox/")])
        self.assertFalse([k for k in plan if k.endswith(".json")])

    def test_collision_lists_every_path(self):
        cfg = self.fixture_copy()
        dup = self.tmp / "fx" / "bigrig" / "02 Homelab" / "Guides"
        dup.mkdir(parents=True)
        (dup / "Build.md").write_text("# Other\n")
        (self.tmp / "fx" / "bigrig" / "Index.md").write_text("# Other\n")
        with self.assertRaises(ComposeError) as cm:
            plan_tree(cfg)
        msg = str(cm.exception)
        self.assertTrue(msg.startswith("collision:"))
        self.assertIn("02 Homelab/Guides/Build.md", msg)
        self.assertIn("\nIndex.md", msg)


class SourceSafety(TempCase):
    def test_protected_and_git_source_paths_are_skipped(self):
        cfg = self.fixture_copy()
        m5 = self.tmp / "fx" / "m5pro"
        (m5 / "README.md").write_text("# Readme\n")
        (m5 / ".git").mkdir()
        (m5 / ".git" / "HEAD").write_text("ref\n")
        plan = plan_tree(cfg)
        self.assertNotIn("README.md", plan)
        self.assertFalse([k for k in plan if k.startswith(".git/")])
        self.assertIn("Index.md", plan)
        self.assertEqual(skipped_protected(cfg), [".git/HEAD", "README.md"])

    def test_symlinked_source_file_is_not_planned(self):
        cfg = self.fixture_copy()
        outside = self.tmp / "outside.md"
        outside.write_text("# Outside\n")
        link = self.tmp / "fx" / "m5pro" / "Link.md"
        link.symlink_to(outside)
        (self.tmp / "fx" / "m5pro" / "Broken.md").symlink_to(self.tmp / "missing.md")
        plan = plan_tree(cfg)
        self.assertNotIn("Link.md", plan)
        self.assertNotIn("Broken.md", plan)


class SyncthingMetadata(TempCase):
    def add_metadata(self, cfg):
        for src in cfg.sources:
            (src.path / ".stignore").write_text("// ignore\n")
            (src.path / ".stfolder").mkdir(exist_ok=True)
            (src.path / ".stfolder" / "marker.txt").write_text("")
            (src.path / ".stversions").mkdir(exist_ok=True)
            (src.path / ".stversions" / "old~.md").write_text("# Old version\n")

    def test_metadata_never_planned_and_two_stignores_do_not_collide(self):
        cfg = self.fixture_copy()
        self.assertNotIn("exclude_files", (self.tmp / "fx" / "compose.yml").read_text())
        self.add_metadata(cfg)
        plan = plan_tree(cfg)
        self.assertFalse([k for k in plan if k.split("/")[-1] == ".stignore"
                          or k.startswith((".stfolder/", ".stversions/"))])

    def test_metadata_excluded_even_when_config_clears_exclude_files(self):
        cfg = dataclasses.replace(self.fixture_copy(), exclude_files=[])
        self.add_metadata(cfg)
        self.assertNotIn(".stignore", plan_tree(cfg))

    def test_count_notes_ignores_versions(self):
        cfg = self.fixture_copy()
        self.add_metadata(cfg)
        self.assertEqual(count_notes(cfg.sources[0].path, cfg.exclude_dirs), 3)
        self.assertEqual(count_notes(cfg.sources[1].path), 3)

    def test_config_reads_exclude_files_with_default(self):
        self.assertEqual(load_config(FIX / "compose.yml").exclude_files, [".stignore"])
        prod = Path(__file__).resolve().parents[2] / "unraid" / "compose.yml"
        cfg = load_config(prod)
        self.assertEqual(cfg.exclude_files, [".stignore"])
        self.assertTrue({".stfolder", ".stversions"} <= set(cfg.exclude_dirs))


class ApplyTree(TempCase):
    def setUp(self):
        super().setUp()
        self.pub = self.tmp / "published"
        self.cfg = dataclasses.replace(load_config(FIX / "compose.yml"), published=self.pub)
        self.plan = plan_tree(self.cfg)

    def test_first_apply_adds_everything(self):
        stats = apply_tree(self.plan, self.cfg)
        self.assertEqual(stats.added, len(self.plan))
        self.assertEqual(stats.removed, 0)
        for rel in self.plan:
            self.assertTrue((self.pub / rel).is_file(), rel)

    def test_second_apply_is_noop(self):
        apply_tree(self.plan, self.cfg)
        self.assertEqual(apply_tree(self.plan, self.cfg), TreeStats(0, 0, 0))

    def test_changed_source_file_is_recopied(self):
        apply_tree(self.plan, self.cfg)
        (self.pub / "Index.md").write_text("tampered, different size\n")
        self.assertEqual(apply_tree(self.plan, self.cfg), TreeStats(0, 1, 0))

    def test_removed_source_file_is_deleted_but_protected_survive(self):
        for rel in (".github/x", "README.md", "garden-manifest.json", "stale.md", "gone/deep/old.md"):
            p = self.pub / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("x")
        stats = apply_tree(self.plan, self.cfg)
        self.assertEqual(stats.removed, 2)
        self.assertFalse((self.pub / "stale.md").exists())
        self.assertFalse((self.pub / "gone").exists())
        for rel in (".github/x", "README.md", "garden-manifest.json"):
            self.assertTrue((self.pub / rel).exists(), rel)

    def test_git_file_untouched(self):
        self.pub.mkdir()
        (self.pub / ".git").write_text("gitdir: elsewhere\n")
        apply_tree(self.plan, self.cfg)
        self.assertTrue((self.pub / ".git").is_file())

    def test_git_dir_untouched(self):
        (self.pub / ".git").mkdir(parents=True)
        (self.pub / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
        apply_tree(self.plan, self.cfg)
        self.assertTrue((self.pub / ".git" / "HEAD").exists())


class GuardSources(TempCase):
    def test_counts_exclude_private_and_inbox(self):
        cfg = self.fixture_copy()
        self.assertEqual(count_notes(cfg.sources[0].path), 3)
        self.assertEqual(count_notes(cfg.sources[1].path), 3)
        guard_sources(cfg, {"m5pro": 3, "bigrig": 3})

    def test_empty_folder_fails_before_planning(self):
        empty = self.tmp / "empty"
        empty.mkdir()
        cfg = load_config(FIX / "compose.yml")
        cfg = dataclasses.replace(cfg, sources=[dataclasses.replace(cfg.sources[0], path=empty), cfg.sources[1]])
        with self.assertRaises(ComposeError) as cm:
            guard_sources(cfg, {})
        self.assertIn("source looks empty: m5pro", str(cm.exception))

    def test_half_of_last_run_fails(self):
        cfg = self.fixture_copy()
        with self.assertRaises(ComposeError) as cm:
            guard_sources(cfg, {"m5pro": 7})
        self.assertEqual(str(cm.exception), "source looks empty: m5pro (3 notes, last 7)")

    def test_missing_folder_fails(self):
        cfg = load_config(FIX / "compose.yml")
        cfg = dataclasses.replace(cfg, sources=[dataclasses.replace(cfg.sources[0], path=self.tmp / "nope")])
        with self.assertRaises(ComposeError) as cm:
            guard_sources(cfg, {"m5pro": 3})
        self.assertIn("source looks empty: m5pro", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
