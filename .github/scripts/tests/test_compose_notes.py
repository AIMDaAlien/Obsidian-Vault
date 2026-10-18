import shutil
import tempfile
import unittest
from pathlib import Path

from composelib import ComposeError
from composelib.notes import (
    CurationEntry, apply_curation, drop_key, first_h1, frontmatter_ranks, get_key,
    join_frontmatter, load_curation, normalize_note, rank_errors, set_key,
    split_frontmatter, validate_curation,
)

FIX = Path(__file__).parent / "fixtures" / "compose"

CODE_NOTE = "---\ntitle: A\npublish: true\n---\n# A\n\n```\n---\nnot: frontmatter\n---\n```\n"

TEXT_WITH_CANDIDATE = (
    "---\n"
    "type: benchmark-log\n"
    "tags:\n"
    "  - llm\n"
    "  - bench\n"
    "featured_candidate: true\n"
    "---\n"
    "# Penthouse Remake\n\nBody text.\n"
)


class TempCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def root_with(self, **notes):
        """Make a published root holding the given {filename: text} notes."""
        root = self.tmp / "pub"
        root.mkdir(exist_ok=True)
        for name, text in notes.items():
            (root / name).write_text(text, encoding="utf-8")
        return root


class Frontmatter(unittest.TestCase):
    def test_set_key_replaces_in_place_and_keeps_order(self):
        out = set_key(["title: A", "publish: true", "tags: []"], "publish", "false")
        self.assertEqual(out, ["title: A", "publish: false", "tags: []"])

    def test_set_key_appends_when_missing(self):
        self.assertEqual(set_key(["title: A"], "machine", "mac"), ["title: A", "machine: mac"])

    def test_set_key_quotes_summary(self):
        out = set_key([], "summary", 'say "hi"')
        self.assertEqual(out, ['summary: "say \\"hi\\""'])

    def test_set_key_replaces_multiline_value(self):
        out = set_key(["tags:", "  - a", "  - b", "publish: true"], "tags", "[]")
        self.assertEqual(out, ["tags: []", "publish: true"])

    def test_get_key_strips_quotes(self):
        self.assertEqual(get_key(['summary: "x"', "a: 'y'", "b: z"], "summary"), "x")
        self.assertEqual(get_key(['summary: "x"', "a: 'y'", "b: z"], "a"), "y")
        self.assertIsNone(get_key(["b: z"], "missing"))

    def test_get_key_ignores_indented_lookalikes(self):
        self.assertIsNone(get_key(["tags:", "  publish: true"], "publish"))

    def test_drop_key_takes_continuation_lines(self):
        out = drop_key(["a: 1", "tags:", "  - x", "b: 2"], "tags")
        self.assertEqual(out, ["a: 1", "b: 2"])

    def test_body_untouched(self):
        lines, body = split_frontmatter(CODE_NOTE)
        self.assertEqual(lines, ["title: A", "publish: true"])
        self.assertEqual(join_frontmatter(lines, body), CODE_NOTE)

    def test_no_frontmatter_is_none(self):
        self.assertEqual(split_frontmatter("# Hi\n"), (None, "# Hi\n"))
        self.assertEqual(split_frontmatter("---\nnever closed\n"), (None, "---\nnever closed\n"))

    def test_first_h1_skips_code_fences(self):
        self.assertEqual(first_h1("```\n# not\n```\n# Real\n## Sub\n"), "Real")
        self.assertIsNone(first_h1("## only h2\n"))


class Normalize(unittest.TestCase):
    def test_bigrig_note_gets_machine_publish_title_and_loses_candidate(self):
        out = normalize_note(TEXT_WITH_CANDIDATE, "bigrig", "2026-10-18")
        lines, _ = split_frontmatter(out)
        self.assertEqual(get_key(lines, "machine"), "bigrig")
        self.assertEqual(get_key(lines, "publish"), "true")
        self.assertEqual(get_key(lines, "title"), "Penthouse Remake")
        self.assertIsNone(get_key(lines, "featured_candidate"))

    def test_existing_publish_false_is_kept(self):
        out = normalize_note("---\npublish: false\n---\n# T\n", "mac", "2026-10-18")
        self.assertEqual(get_key(split_frontmatter(out)[0], "publish"), "false")

    def test_existing_machine_and_title_kept(self):
        out = normalize_note("---\nmachine: other\ntitle: Mine\n---\n# T\n", "mac", "2026-10-18")
        lines, _ = split_frontmatter(out)
        self.assertEqual(get_key(lines, "machine"), "other")
        self.assertEqual(get_key(lines, "title"), "Mine")

    def test_no_h1_means_no_title(self):
        out = normalize_note("---\npublish: true\n---\njust text\n", "mac", "2026-10-18")
        self.assertIsNone(get_key(split_frontmatter(out)[0], "title"))

    def test_no_frontmatter_gets_minimum_block(self):
        out = normalize_note("# Plain\n\nText\n", "bigrig", "2026-10-18")
        lines, body = split_frontmatter(out)
        self.assertEqual(lines, ["tags: []", "created: 2026-10-18", "publish: true",
                                 "machine: bigrig", "title: Plain"])
        self.assertEqual(body, "# Plain\n\nText\n")

    def test_other_keys_untouched(self):
        out = normalize_note(TEXT_WITH_CANDIDATE, "bigrig", "2026-10-18")
        lines, body = split_frontmatter(out)
        self.assertEqual(lines[:4], ["type: benchmark-log", "tags:", "  - llm", "  - bench"])
        self.assertEqual(body, "# Penthouse Remake\n\nBody text.\n")

    def test_fixture_note_round_trips_outside_touched_keys(self):
        text = (FIX / "bigrig" / "01 Projects" / "The Penthouse" / "Penthouse Remake.md").read_text()
        out = normalize_note(text, "bigrig", "2026-10-18")
        self.assertEqual(split_frontmatter(out)[1], split_frontmatter(text)[1])


class CurationTests(TempCase):
    def entry(self, path, **kw):
        return CurationEntry(path, kw.get("featured"), kw.get("summary"), kw.get("publish"))

    def test_load_entries(self):
        p = self.tmp / "curation.yml"
        p.write_text('- path: "A.md"\n  featured: 2\n  summary: "s"\n- path: B.md\n  publish: false\n')
        self.assertEqual(load_curation(p), [
            CurationEntry("A.md", 2, "s", None),
            CurationEntry("B.md", None, None, False),
        ])

    def test_load_rejects_unknown_key(self):
        p = self.tmp / "curation.yml"
        p.write_text("- path: A.md\n  rank: 2\n")
        with self.assertRaises(ComposeError) as cm:
            load_curation(p)
        self.assertIn("A.md: unknown key rank", str(cm.exception))

    def test_unknown_path_is_error(self):
        root = self.root_with(**{"A.md": "# A\n"})
        errs = validate_curation([self.entry("Nope.md", featured=1)], root, {})
        self.assertEqual(errs, ["unknown path: Nope.md"])

    def test_duplicate_rank_is_error(self):
        root = self.root_with(**{"A.md": "# A\n", "B.md": "# B\n"})
        errs = validate_curation([self.entry("A.md", featured=2), self.entry("B.md", featured=2)], root, {})
        self.assertEqual(errs, ["duplicate rank 2: A.md, B.md"])

    def test_rank_clash_with_frontmatter_is_error(self):
        root = self.root_with(**{"A.md": "# A\n", "M.md": "---\nfeatured: 3\n---\n"})
        errs = validate_curation([self.entry("A.md", featured=3)], root, {"M.md": 3})
        self.assertEqual(errs, ["rank 3 already used by M.md"])

    def test_entry_may_restate_its_own_frontmatter_rank(self):
        root = self.root_with(**{"M.md": "---\nfeatured: 3\n---\n"})
        self.assertEqual(validate_curation([self.entry("M.md", featured=3)], root, {"M.md": 3}), [])

    def test_summary_over_160_is_error(self):
        root = self.root_with(**{"A.md": "# A\n"})
        long = "x" * 161
        self.assertEqual(validate_curation([self.entry("A.md", summary=long)], root, {}),
                         ["summary too long (161 > 160): A.md"])
        self.assertEqual(validate_curation([self.entry("A.md", summary="x" * 160)], root, {}), [])

    def test_non_positive_rank_is_error(self):
        root = self.root_with(**{"A.md": "# A\n"})
        errs = validate_curation([self.entry("A.md", featured=0)], root, {})
        self.assertEqual(len(errs), 1)
        self.assertIn("A.md", errs[0])

    def test_non_integer_frontmatter_rank_reported(self):
        for raw in ('"3"', "yes", "2.5", "0"):
            root = self.root_with(**{"A.md": f"---\nfeatured: {raw}\n---\n# A\n"})
            errs = rank_errors(root)
            self.assertEqual(len(errs), 1, raw)
            self.assertIn("featured must be an integer", errs[0])
            self.assertTrue(errs[0].startswith("A.md: "))

    def test_valid_and_absent_ranks_not_reported(self):
        root = self.root_with(**{"A.md": "---\nfeatured: 4\n---\n", "B.md": "# B\n"})
        self.assertEqual(rank_errors(root), [])

    def test_frontmatter_ranks_only_for_mac_paths(self):
        root = self.root_with(**{"A.md": "---\nfeatured: 4\n---\n", "B.md": "---\nfeatured: 5\n---\n",
                                 "C.md": "---\nfeatured: yes\n---\n"})
        self.assertEqual(frontmatter_ranks(root, {"A.md", "C.md"}), {"A.md": 4})

    def test_apply_sets_featured_summary_publish(self):
        text = "---\ntype: guide\npublish: true\n---\n# A\n"
        out = apply_curation(text, CurationEntry("A.md", 2, 'A "good" one', False))
        lines, body = split_frontmatter(out)
        self.assertEqual(get_key(lines, "featured"), "2")
        self.assertEqual(get_key(lines, "summary"), 'A "good" one')
        self.assertIn('summary: "A \\"good\\" one"', lines)
        self.assertEqual(get_key(lines, "publish"), "false")
        self.assertEqual(get_key(lines, "type"), "guide")
        self.assertEqual(body, "# A\n")

    def test_apply_leaves_unset_keys_alone(self):
        text = '---\nsummary: "keep"\n---\nx\n'
        out = apply_curation(text, CurationEntry("A.md", 1, None, None))
        lines, _ = split_frontmatter(out)
        self.assertEqual(get_key(lines, "summary"), "keep")
        self.assertEqual(get_key(lines, "featured"), "1")

    def test_apply_to_note_without_frontmatter_creates_block(self):
        out = apply_curation("# A\n", CurationEntry("A.md", 1, None, None))
        self.assertEqual(out, "---\nfeatured: 1\n---\n# A\n")


if __name__ == "__main__":
    unittest.main()
