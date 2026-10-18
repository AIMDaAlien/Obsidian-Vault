import tempfile
import unittest
from pathlib import Path

from composelib.links import WIKILINK_RE, build_index, resolve_bare_embeds, unwrap_excluded_links

EXT = "json jsonl log csv py sh patch txt exit-code".split()


class Index(unittest.TestCase):
    def test_maps_lowercase_basename_to_sorted_paths_and_skips_protected(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for rel in ["_attachments/run3/Remake.png", "_attachments/run2/remake.png",
                        "notes/A.md", ".git/objects/remake.png", ".github/scripts/remake.png"]:
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text("x")
            idx = build_index(root)
        self.assertEqual(idx["remake.png"], ["_attachments/run2/remake.png", "_attachments/run3/Remake.png"])
        self.assertEqual(idx["a.md"], ["notes/A.md"])


class Embeds(unittest.TestCase):
    def test_unique_bare_embed_gets_full_path(self):
        out, bad = resolve_bare_embeds("![[lcb60-pareto.png]]", {"lcb60-pareto.png": ["_attachments/run1/lcb60-pareto.png"]})
        self.assertEqual(out, "![[_attachments/run1/lcb60-pareto.png]]"); self.assertEqual(bad, [])

    def test_ambiguous_bare_embed_left_and_reported(self):
        out, bad = resolve_bare_embeds("![[remake.png]]", {"remake.png": ["_attachments/run2/remake.png", "_attachments/run3/remake.png"]})
        self.assertEqual(out, "![[remake.png]]")
        self.assertEqual(bad, ["remake.png (ambiguous: _attachments/run2/remake.png, _attachments/run3/remake.png)"])

    def test_missing_reported(self):
        out, bad = resolve_bare_embeds("![[gone.png]]", {})
        self.assertEqual(out, "![[gone.png]]"); self.assertEqual(bad, ["gone.png (missing)"])

    def test_pathed_embed_untouched(self):
        t = "![[_attachments/x/y.png]]"
        self.assertEqual(resolve_bare_embeds(t, {"y.png": ["other/y.png"]}), (t, []))

    def test_markdown_image_syntax_untouched(self):
        t = "![alt](images/pi.png)"
        self.assertEqual(resolve_bare_embeds(t, {"pi.png": ["images/pi.png"]}), (t, []))

    def test_size_and_anchor_suffix_kept(self):
        idx = {"c.png": ["a/c.png"]}
        self.assertEqual(resolve_bare_embeds("![[c.png|400]] ![[c.png#x]]", idx)[0], "![[a/c.png|400]] ![[a/c.png#x]]")

    def test_non_image_and_note_embeds_untouched(self):
        t = "![[Some Note]] ![[doc.pdf]]"
        self.assertEqual(resolve_bare_embeds(t, {}), (t, []))

    def test_code_is_skipped(self):
        idx = {"c.png": ["a/c.png"]}
        t = "```\n![[c.png]]\n```\n`![[c.png]]` ![[c.png]]"
        self.assertEqual(resolve_bare_embeds(t, idx)[0], "```\n![[c.png]]\n```\n`![[c.png]]` ![[a/c.png]]")

    def test_tilde_fence_skipped_and_prose_after_transformed(self):
        idx = {"c.png": ["a/c.png"]}
        t = "~~~\n![[c.png]]\n~~~\n![[c.png]]"
        self.assertEqual(resolve_bare_embeds(t, idx)[0], "~~~\n![[c.png]]\n~~~\n![[a/c.png]]")


class Unwrap(unittest.TestCase):
    def test_json_link_becomes_text(self):
        out, done = unwrap_excluded_links("see [[_attachments/run1/results.json|the results]]", {}, EXT)
        self.assertEqual(out, "see the results"); self.assertEqual(done, ["_attachments/run1/results.json"])

    def test_no_alias_uses_basename(self):
        out, done = unwrap_excluded_links("[[_attachments/run1/results.json]]", {}, EXT)
        self.assertEqual(out, "results"); self.assertEqual(done, ["_attachments/run1/results.json"])

    def test_note_link_without_extension_untouched(self):
        t = "[[Planned Note]] and [[Version 1.2 notes]]"
        self.assertEqual(unwrap_excluded_links(t, {}, EXT), (t, []))

    def test_table_escaped_pipe_preserved(self):
        t = "| [[Flash-Next AD384\\|Flash]] | 54/60 |"
        self.assertEqual(unwrap_excluded_links(t, {}, EXT), (t, []))

    def test_table_unwrap_uses_alias(self):
        out, done = unwrap_excluded_links("| [[x/r.csv\\|data]] | 1 |", {}, EXT)
        self.assertEqual(out, "| data | 1 |"); self.assertEqual(done, ["x/r.csv"])

    def test_png_present_in_index_untouched(self):
        t = "![[a/c.png]]"
        self.assertEqual(unwrap_excluded_links(t, {"c.png": ["a/c.png"]}, EXT), (t, []))

    def test_png_absent_from_index_unwrapped(self):
        out, done = unwrap_excluded_links("x ![[a/c.png]] y", {}, EXT)
        self.assertEqual(out, "x c y"); self.assertEqual(done, ["a/c.png"])

    def test_dotted_note_names_untouched(self):
        for idx in ({}, {"node.js.md": ["Node.js.md"]}):
            for t in ("[[Node.js]]", "[[llama.cpp]]", "[[Next.js]]", "[[ASP.NET]]"):
                self.assertEqual(unwrap_excluded_links(t, idx, EXT), (t, []))

    def test_chart_png_absent_unwrapped_present_kept(self):
        self.assertEqual(unwrap_excluded_links("[[chart.png]]", {}, EXT), ("chart", ["chart.png"]))
        t = "[[chart.png]]"
        self.assertEqual(unwrap_excluded_links(t, {"chart.png": ["x/chart.png"]}, EXT), (t, []))

    def test_markdown_target_untouched(self):
        t = "[[a/b.md]]"
        self.assertEqual(unwrap_excluded_links(t, {}, EXT), (t, []))

    def test_embed_size_not_used_as_text(self):
        out, _ = unwrap_excluded_links("![[a/c.png|400]]", {}, EXT)
        self.assertEqual(out, "c")

    def test_anchor_dropped_and_code_skipped(self):
        out, done = unwrap_excluded_links("[[r.log#L3]] `[[r.log]]`\n```\n[[r.log]]\n```", {}, EXT)
        self.assertEqual(out, "r `[[r.log]]`\n```\n[[r.log]]\n```"); self.assertEqual(done, ["r.log"])

    def test_document_order(self):
        _, done = unwrap_excluded_links("[[b.json]] [[a.csv]]", {}, EXT)
        self.assertEqual(done, ["b.json", "a.csv"])


class Regex(unittest.TestCase):
    def test_groups_keep_escaped_pipe(self):
        m = WIKILINK_RE.search("[[T\\|alias]]")
        self.assertEqual(m.groups(), ("", "T", None, "\\|", "alias"))


if __name__ == "__main__":
    unittest.main()
