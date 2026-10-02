"""Portable subprocess checks for the local CLI; no external calls."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GOOD = 'The server sends data.'
BAD = 'It is worth noting that this is potentially useful.'


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='eidetic-cli-test-')
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def run_cli(self, *args, direct=False, stdin=None, cwd=None):
        invocation = [str(ROOT / 'validator/validate.py')] if direct else ['-m', 'validator.validate']
        env = {**os.environ, 'PYTHONUTF8': '0', 'PYTHONIOENCODING': 'cp1252'}
        return subprocess.run([sys.executable, '-X', 'utf8=0', *invocation, *map(str, args)],
                              cwd=cwd or ROOT, env=env, input=stdin, capture_output=True,
                              text=True, encoding='utf-8', timeout=10)

    def test_module_success_json_and_modes(self):
        for mode in ('terse', 'balanced', 'expanded'):
            with self.subTest(mode=mode):
                result = self.run_cli('--text', GOOD, '--mode', mode, '--json')
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(result.stdout)
                self.assertTrue(report['pass'])
                self.assertEqual(report['mode'], mode)

    def test_direct_script_works_outside_repository(self):
        result = self.run_cli('--text', GOOD, '--json', direct=True, cwd=self.directory)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['pass'])

    def test_failed_heuristic_report_has_nonzero_exit(self):
        for json_output in (False, True):
            with self.subTest(json=json_output):
                result = self.run_cli('--text', BAD, *(['--json'] if json_output else []))
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                if json_output:
                    self.assertFalse(json.loads(result.stdout)['pass'])
                else:
                    self.assertIn('FAIL', result.stdout)
                self.assertNotIn('Traceback', result.stderr)

    def test_utf8_file_path_and_report_work_with_legacy_windows_encoding(self):
        source = self.directory / 'fictional-\u96ea.md'
        source.write_text(BAD + ' \u96ea', encoding='utf-8')
        result = self.run_cli('--input', source, direct=True, cwd=self.directory)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('\u96ea', result.stdout)
        self.assertNotIn('Traceback', result.stderr)

    def test_stdin_accepts_utf8_and_preserves_json_report(self):
        result = self.run_cli('--json', stdin=BAD + ' \u96ea')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report['pass'])
        self.assertIn('\u96ea', '\n'.join(item['text'] for item in report['claim_failures']))

    def test_missing_and_invalid_utf8_files_have_clear_input_errors(self):
        invalid = self.directory / 'invalid.md'
        invalid.write_bytes(b'\xff\xfe')
        for source in (self.directory / 'missing-\u96ea.md', invalid):
            with self.subTest(source=source):
                result = self.run_cli('--input', source, '--json')
                self.assertEqual(result.returncode, 2)
                self.assertIn('Cannot read input', json.loads(result.stdout)['error'])
                self.assertNotIn('Traceback', result.stderr)

    def test_empty_and_conflicting_inputs_fail_instead_of_waiting_or_succeeding(self):
        for args in (('--text', ''), ('--text', GOOD, '--input', 'missing.md')):
            result = self.run_cli(*args, stdin='')
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertNotIn('Traceback', result.stderr)

    def test_invalid_mode_is_a_usage_error(self):
        result = self.run_cli('--text', GOOD, '--mode', 'unknown')
        self.assertEqual(result.returncode, 2)
        self.assertIn('invalid choice', result.stderr)


if __name__ == '__main__':
    unittest.main()
