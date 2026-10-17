import contextlib
import importlib.util
import io
import os
import re
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
GENERATOR_PATH = os.path.join(HERE, '..', 'generate-manifest.py')
FX = os.path.join(HERE, 'fixtures', 'manifest')


def load_generator():
    spec = importlib.util.spec_from_file_location('generate_manifest', GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gm = load_generator()


def read(name):
    with open(os.path.join(FX, name), encoding='utf-8') as f:
        return f.read()


class ParseFrontmatterTests(unittest.TestCase):
    def test_inline_list_and_int(self):
        fm, _ = gm.parse_frontmatter(read('inline.md'))
        self.assertEqual(fm['tags'], ['a', 'b'])
        self.assertEqual(fm['featured'], 3)
        self.assertIs(fm['publish'], True)

    def test_block_list(self):
        fm, _ = gm.parse_frontmatter(read('block.md'))
        self.assertEqual(fm['tags'], ['x', 'y'])

    def test_quoted_date_string(self):
        fm, _ = gm.parse_frontmatter(read('quoted.md'))
        self.assertEqual(fm['created'], '2025-01-02')
        self.assertEqual(fm['updated'], '2026-02-03')

    def test_title_precedence(self):
        titles = {}
        for name in ('inline.md', 'block.md', 'none.md'):
            fm, body = gm.parse_frontmatter(read(name))
            titles[name] = gm.extract_title(fm, body, name)
        self.assertEqual(titles['inline.md'], 'Custom')
        self.assertEqual(titles['block.md'], 'Block Heading')
        self.assertEqual(titles['none.md'], 'none')

    def test_extract_links(self):
        _, body = gm.parse_frontmatter(read('inline.md'))
        self.assertEqual(gm.extract_links(body), ['Target One', 'Other'])
        text = '```\n[[Hidden]]\n```\n![[pic.png]] ![[Note Embed]] [[Seen]]'
        self.assertEqual(gm.extract_links(text), ['Note Embed', 'Seen'])


class ParserEdgeCaseTests(unittest.TestCase):
    def test_crlf(self):
        fm, body = gm.parse_frontmatter('---\r\ntags: [a]\r\n---\r\nbody')
        self.assertEqual(fm, {'tags': ['a']})
        self.assertEqual(body, 'body')

    def test_malformed_lines_skipped(self):
        fm, _ = gm.parse_frontmatter('---\ntags: [a]\nthis is not yaml\n: nope\nx\n---\nbody')
        self.assertEqual(fm, {'tags': ['a']})

    def test_false_null_empty_list(self):
        fm, _ = gm.parse_frontmatter('---\na: false\nb: null\nc: []\n---\n')
        self.assertEqual(fm, {'a': False, 'b': None, 'c': []})

    def test_quoted_list_items(self):
        fm, _ = gm.parse_frontmatter('---\ntags: ["a", \'b\']\n---\n')
        self.assertEqual(fm['tags'], ['a', 'b'])

    def test_quoted_true_is_string(self):
        fm, _ = gm.parse_frontmatter('---\npublish: "true"\n---\n')
        self.assertEqual(fm['publish'], 'true')

    def test_bom_does_not_disable_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, 'bom.md'), 'w', encoding='utf-8-sig') as f:
                f.write('---\ntitle: Bom\n---\nbody')
            self.assertEqual(gm.build_manifest(tmp)['metadata']['bom.md']['title'], 'Bom')


class BuildManifestTests(unittest.TestCase):
    def test_build_manifest_tree(self):
        # _private/ is itself gitignored in the vault, so recreate it in a copy.
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, 'vault')
            shutil.copytree(FX, root)
            os.makedirs(os.path.join(root, '_private'))
            with open(os.path.join(root, '_private', 'p.md'), 'w') as f:
                f.write('private\n')
            paths = [e['path'] for e in gm.build_manifest(root)['tree']]
        self.assertNotIn('skip.base', paths)
        self.assertNotIn('_private/p.md', paths)
        self.assertIn('inline.md', paths)

    def test_updated_absent_without_git(self):
        # Copy out of the enclosing git repo so history cannot leak in.
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copy(os.path.join(FX, 'inline.md'), tmp)
            metadata = gm.build_manifest(tmp)['metadata']
        self.assertNotIn('updated', metadata['inline.md'])

    def test_updated_from_git(self):
        env = dict(os.environ, GIT_AUTHOR_DATE='2026-01-05T12:00:00',
                   GIT_COMMITTER_DATE='2026-01-05T12:00:00')
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, 'a.md'), 'w') as f:
                f.write('# A\n')
            with open(os.path.join(tmp, 'b.md'), 'w') as f:
                f.write('---\nupdated: 2024-04-04\n---\n# B\n')
            with open(os.path.join(tmp, 'c.md'), 'w') as f:
                f.write('---\nupdated:\n---\n# C\n')
            with open(os.path.join(tmp, 'd[1].md'), 'w') as f:
                f.write('# D\n')
            for args in (['init', '-q'], ['config', 'user.name', 'T'],
                         ['config', 'user.email', 't@example.com'],
                         ['add', '.'], ['-c', 'commit.gpgsign=false', 'commit', '-q', '-m', 'x']):
                subprocess.run(['git', '-C', tmp] + args, check=True, env=env)
            metadata = gm.build_manifest(tmp)['metadata']
        self.assertEqual(metadata['a.md']['updated'], '2026-01-05')
        self.assertEqual(metadata['c.md']['updated'], '2026-01-05')
        self.assertEqual(metadata['d[1].md']['updated'], '2026-01-05')
        self.assertEqual(metadata['b.md']['updated'], '2024-04-04')

    def test_summary_counts_publish(self):
        out = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copy(os.path.join(FX, 'inline.md'), tmp)
            shutil.copy(os.path.join(FX, 'none.md'), tmp)
            with contextlib.redirect_stdout(out):
                self.assertEqual(gm.main([tmp]), 0)
            self.assertTrue(os.path.exists(os.path.join(tmp, 'garden-manifest.json')))
        self.assertRegex(out.getvalue().strip(), re.compile(
            r'^Manifest generated: \d+ files, \d+ dirs, \d+ publishable notes, '
            r'\d+ links across \d+ notes$'))
        self.assertIn('1 publishable notes', out.getvalue())

    def test_quoted_publish_not_counted(self):
        out = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, 'q.md'), 'w') as f:
                f.write('---\npublish: "true"\n---\n')
            with contextlib.redirect_stdout(out):
                gm.main([tmp])
        self.assertIn(' 0 publishable notes', out.getvalue())


if __name__ == '__main__':
    unittest.main()
