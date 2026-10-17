import contextlib
import importlib.util
import io
import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
GATE_PATH = os.path.join(HERE, '..', 'privacy-gate.py')
HOOK_PATH = os.path.join(HERE, '..', '..', 'hooks', 'pre-commit')
FIXTURES = os.path.join(HERE, 'fixtures', 'gate')
ZERO_REF = '0' * 40


def load_gate():
    spec = importlib.util.spec_from_file_location('privacy_gate', GATE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gate = load_gate()

CASES = [
    ('lan_ip', 'lan.md'), ('public_ip', 'public.md'), ('mac', 'mac.md'),
    ('tailscale_auth', 'tailscale.md'), ('duckdns', 'duckdns.md'),
    ('ts_net', 'tsnet.md'), ('phone', 'phone.md'), ('private_key', 'key.md'),
    ('tskey', 'tskey.md'), ('github_token', 'ghp.md'), ('aws_key', 'akia.md'),
    ('discord_webhook', 'discord.md'), ('home_path', 'home.md'),
    ('sshpass', 'sshpass.md'), ('env_unraid', 'env.md'),
    ('private_deployment', 'deploy.md'),
]


def read(name):
    with open(os.path.join(FIXTURES, name), encoding='utf-8') as f:
        return f.read()


def git(cwd, *args):
    subprocess.run(
        ['git', '-c', 'user.name=t', '-c', 'user.email=t@example.com', *args],
        cwd=cwd, check=True, capture_output=True)


class ScanTextTests(unittest.TestCase):
    def test_clean_has_no_hits(self):
        self.assertEqual(gate.scan_text(read('clean.md'), 'clean.md', []), [])

    def test_each_pattern_once(self):
        for name, file in CASES:
            hits = gate.scan_text(read(file), file, [])
            self.assertEqual([h[2] for h in hits], [name], file)

    def test_extra_terms(self):
        self.assertEqual(gate.scan_text('met Jane Roe today', 'x.md', ['Jane Roe']),
                         [('x.md', 1, 'extra_term')])
        self.assertEqual(gate.scan_text('met JANE  roe today', 'x.md', ['Jane Roe']),
                         [('x.md', 1, 'extra_term')])
        self.assertEqual(gate.scan_text('Jane Roebuck', 'x.md', ['Jane Roe']), [])

    def test_line_numbers(self):
        hits = gate.scan_text('ok\nok\n192.168.0.5\n', 'x.md', [])
        self.assertEqual(hits, [('x.md', 3, 'lan_ip')])

    def test_fenced_code_still_scanned(self):
        text = '```\nssh 192.168.0.5\n```\n'
        self.assertEqual(gate.scan_text(text, 'x.md', []), [('x.md', 2, 'lan_ip')])

    def test_ip_rules(self):
        scan = lambda s: [h[2] for h in gate.scan_text(s, 'x.md', [])]
        self.assertEqual(scan('10.0.0.0/8 and 192.168.1.0/24'), [])
        self.assertEqual(scan('192.168.0.50/24'), ['lan_ip'])
        self.assertEqual(scan('10.1.2.3/8'), ['lan_ip'])
        self.assertEqual(scan('10.1.2.3/33'), ['lan_ip'])
        self.assertEqual(scan('http://203.0.113.9/1/admin'), ['public_ip'])
        self.assertEqual(scan('http://10.1.2.3/1/admin'), ['lan_ip'])
        self.assertEqual(scan('172.16.4.0/22'), [])
        self.assertEqual(scan('version 192.168.7.7'), ['lan_ip'])
        self.assertEqual(scan('1.2.3.4'), ['public_ip'])  # no single-digit exemption
        self.assertEqual(scan('999.1.1.1 and 01.2.3.4 and 10.01.2.3'), [])
        self.assertEqual(scan('127.5.5.5 and 192.168.9.0'), [])
        self.assertEqual(scan('Build server 192.168.0.5'), ['lan_ip'])
        self.assertEqual(scan('LGUP 1.16.0.3'), [])
        self.assertEqual(scan('firmware 52.1.2.3'), [])
        self.assertEqual(scan('wan 98.12.4.5'), ['public_ip'])
        self.assertEqual(scan('lan 172.20.1.9'), ['lan_ip'])

    def test_version_word_must_directly_precede(self):
        scan = lambda s: [h[2] for h in gate.scan_text(s, 'x.md', [])]
        for s in ('version: 52.1.2.3', 'Firmware v52.1.2.3', 'BIOS  2.1.0.52', 'kdz:v5.1.2.3'):
            self.assertEqual(scan(s), [], s)
        self.assertEqual(scan('version of the server at 52.1.2.3'), ['public_ip'])
        self.assertEqual(scan('build host is 52.1.2.3'), ['public_ip'])
        self.assertEqual(scan('prebuild 52.1.2.3'), ['public_ip'])
        self.assertEqual(scan('v 1.16.0.3'), ['public_ip'])
        self.assertEqual(scan('version 10.1.2.3'), ['lan_ip'])

    def test_private_key_forms(self):
        scan = lambda s: [h[2] for h in gate.scan_text(s, 'x.md', [])]
        for s in ('-----BEGIN PGP PRIVATE KEY BLOCK-----', '-----BEGIN OPENSSH PRIVATE KEY-----',
                  '-----BEGIN PRIVATE KEY-----'):
            self.assertEqual(scan(s), ['private_key'], s)
        self.assertEqual(scan('-----BEGIN PGP PUBLIC KEY BLOCK-----'), [])

    def test_mac_edges(self):
        scan = lambda s: [h[2] for h in gate.scan_text(s, 'x.md', [])]
        for s in ('MAC:02:00:00:aa:bb:cc', 'ether 02-00-00-AA-BB-CC', '(02:00:00:aa:bb:cc)',
                  'mac=02:00:00:aa:bb:cc:'):
            self.assertEqual(scan(s), ['mac'], s)
        for s in ('50:01:43:80:12:34:56:78', 'wwn 50:01:43:80:12:34:56', 'x 10:20:30:40:50:60:70'):
            self.assertEqual(scan(s), [], s)

    def test_host_patterns_case_insensitive(self):
        scan = lambda s: [h[2] for h in gate.scan_text(s, 'x.md', [])]
        self.assertEqual(scan('box.DuckDNS.org'), ['duckdns'])
        self.assertEqual(scan('node.tail1234.TS.NET'), ['ts_net'])

    def test_github_token_prefixes(self):
        scan = lambda s: [h[2] for h in gate.scan_text(s, 'x.md', [])]
        for prefix in ('ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_'):
            self.assertEqual(scan(prefix + 'A1b2' * 9), ['github_token'], prefix)
        self.assertEqual(scan('ghx_' + 'A1b2' * 9), [])

    def test_phone_forms(self):
        for s in ('(571) 777-0199', '571-777-0199', '571.777.0199', '571 777 0199',
                  '1-571-777-0199', '+1-571-777-0199', '+1 (571) 777-0199'):
            self.assertEqual([h[2] for h in gate.scan_text(s, 'x.md', [])], ['phone'], s)
        for s in ('571-555-0199', '(571) 555-0199', '555-123-4567', '1-555-123-4567'):
            self.assertEqual(gate.scan_text(s, 'x.md', []), [], s)

    def test_phone_unseparated(self):
        self.assertEqual([h[2] for h in gate.scan_text('call 5717770199', 'x.md', [])], ['phone'])
        for s in ('5551234567', '5715550199', 'sha 3f9a2b7c1d', 'commit 1234567890abcdef',
                  '57177701990', 'id a5717770199'):
            self.assertEqual(gate.scan_text(s, 'x.md', []), [], s)

    def test_home_path_placeholders(self):
        for s in ('/Users/USERNAME/x', '/Users/<you>/x', '/Users/you/x'):
            self.assertEqual(gate.scan_text(s, 'x.md', []), [], s)
        self.assertEqual([h[2] for h in gate.scan_text('C:\\Users\\bob\\x', 'x.md', [])],
                         ['home_path'])
        self.assertEqual(gate.scan_text('GET api/Users/list', 'x.md', []), [])
        for s in ('(/Users/bob/x)', 'path=/Users/bob', '"/Users/bob"', '`/Users/bob`',
                  'file:///Users/bob/x', '[/Users/bob/x]', '~/Users/bob', '/Users/bob',
                  'C:\\\\Users\\\\bob', 'c:\\users\\bob', 'C:\\USERS\\bob'):
            self.assertEqual([h[2] for h in gate.scan_text(s, 'x.md', [])], ['home_path'], s)
        for s in ('api/Users/bob', 'x\\/Users/bob'):
            self.assertEqual(gate.scan_text(s, 'x.md', []), [], s)

    def test_load_extra_terms(self):
        self.assertEqual(gate.load_extra_terms('/nonexistent/terms'), [])
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'terms')
            with open(p, 'w', encoding='utf-8') as f:
                f.write('# comment\nJane Roe\n\n  admin1  \n')
            self.assertEqual(gate.load_extra_terms(p), ['Jane Roe', 'admin1'])


class RepoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        git(self.tmp, 'init', '-q', '-b', 'main')
        self.put('clean.md', read('clean.md'))
        git(self.tmp, 'add', '-A')
        git(self.tmp, 'commit', '-q', '-m', 'init')
        saved = gate.TERMS_PATH
        gate.TERMS_PATH = os.path.join(self.tmp, 'no-such-terms')
        self.addCleanup(setattr, gate, 'TERMS_PATH', saved)

    def put(self, name, content, binary=False):
        with open(os.path.join(self.tmp, name), 'wb' if binary else 'w') as f:
            f.write(content)

    def run_main(self, *extra):
        out, self.err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(self.err):
            code = gate.main(['--root', self.tmp, *extra])
        return code, out.getvalue()

    def test_main_exit_codes(self):
        code, out = self.run_main()
        self.assertEqual((code, out), (0, 'privacy gate: clean, 1 files\n'))
        self.put('lan.md', read('lan.md'))
        git(self.tmp, 'add', 'lan.md')
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn('lan.md:1: lan_ip', out)
        self.assertTrue(out.endswith('privacy gate: 1 hits\n'))

    def test_untracked_ignored(self):
        self.put('lan.md', read('lan.md'))
        self.assertEqual(self.run_main()[0], 0)

    def test_self_paths_skipped(self):
        os.makedirs(os.path.join(self.tmp, '.github', 'scripts', 'tests', 'fixtures', 'gate'))
        self.put('.github/scripts/tests/fixtures/gate/lan.md', read('lan.md'))
        self.put('.github/scripts/tests/test_privacy_gate.py', read('lan.md'))
        git(self.tmp, 'add', '-A')
        self.assertEqual(self.run_main()[0], 0)

    def test_only_listed_self_paths_skipped(self):
        os.makedirs(os.path.join(self.tmp, '.github', 'scripts', 'tests', '__pycache__'))
        self.put('.github/scripts/privacy-gate.py', read('lan.md'))
        self.put('.github/scripts/tests/t.md', read('lan.md'))
        self.put('.github/scripts/tests/__pycache__/x.txt', read('lan.md'))
        git(self.tmp, 'add', '-A')
        code, out = self.run_main()
        self.assertEqual(code, 1)
        for p in ('.github/scripts/privacy-gate.py', '.github/scripts/tests/t.md',
                  '.github/scripts/tests/__pycache__/x.txt'):
            self.assertIn(p + ':1: lan_ip', out)

    def test_symlink_target_scanned(self):
        os.symlink('/Users/bob/notes', os.path.join(self.tmp, 'link'))
        git(self.tmp, 'add', 'link')
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn('link:1: home_path', out)

    def test_any_extension_scanned(self):
        self.put('notes.canvas', '{"text": "nas at 192.168.0.5"}')
        git(self.tmp, 'add', 'notes.canvas')
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn('notes.canvas:1: lan_ip', out)

    def test_binary_blob_skipped(self):
        self.put('mod.pyc', b'\x00\x01 192.168.0.5 /Users/bob', binary=True)
        git(self.tmp, 'add', 'mod.pyc')
        self.assertEqual(self.run_main(), (0, 'privacy gate: clean, 1 files\n'))

    def test_index_not_working_tree(self):
        self.put('clean.md', read('lan.md'))  # unstaged edit: not what would be committed
        self.assertEqual(self.run_main()[0], 0)
        git(self.tmp, 'add', 'clean.md')
        self.assertEqual(self.run_main()[0], 1)
        self.put('clean.md', read('clean.md'))  # staged hit, clean working tree
        self.assertEqual(self.run_main()[0], 1)

    def test_missing_terms_note(self):
        self.assertEqual(self.run_main()[0], 0)
        self.assertIn('privacy gate: note: no ~/.vault-privacy-terms, extra terms not checked',
                      self.err.getvalue())
        terms = os.path.join(self.tmp, 'terms')
        with open(terms, 'w', encoding='utf-8') as f:
            f.write('Jane Roe\n')
        gate.TERMS_PATH = terms
        self.run_main()
        self.assertNotIn('note:', self.err.getvalue())

    def test_new_images_staged(self):
        self.put('new.png', b'x', binary=True)
        self.assertEqual(gate.new_images(self.tmp, None), ['new.png'])
        git(self.tmp, 'add', 'new.png')
        self.assertEqual(gate.new_images(self.tmp, None), ['new.png'])

    def test_new_images_base_ref(self):
        self.put('new.png', b'x', binary=True)
        git(self.tmp, 'add', '-A')
        git(self.tmp, 'commit', '-q', '-m', 'img')
        self.assertEqual(gate.new_images(self.tmp, 'HEAD~1'), ['new.png'])
        self.assertEqual(gate.new_images(self.tmp, ZERO_REF), [])
        self.assertEqual(gate.new_images(self.tmp, 'no-such-ref'), [])

    def test_images_reported_without_changing_exit(self):
        self.put('new.png', b'x', binary=True)
        git(self.tmp, 'add', 'new.png')
        code, out = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn('review image: new.png', out)

    def test_non_repo_root_fails_closed(self):
        with tempfile.TemporaryDirectory() as d, contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(gate.main(['--root', d]), 2)
        self.assertIn('git error', err.getvalue())

    def test_no_tracked_text_files_fails(self):
        git(self.tmp, 'rm', '-q', 'clean.md')
        self.assertEqual(self.run_main()[0], 2)

    def test_zero_base_ref_via_main(self):
        self.assertEqual(self.run_main('--base-ref', ZERO_REF)[0], 0)


class HookTests(unittest.TestCase):
    def test_pre_commit_hook_runs_gate(self):
        self.assertTrue(os.access(HOOK_PATH, os.X_OK))
        with open(HOOK_PATH, encoding='utf-8') as f:
            self.assertIn('privacy-gate.py', f.read())


if __name__ == '__main__':
    unittest.main()
