from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/install.py'


class InstallTests(unittest.TestCase):
    def test_preview_then_install_and_idempotent_merge(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            target.mkdir()
            entry = target / 'agent.md'
            entry.write_text('# Existing user rules\n')
            args = [sys.executable, str(SCRIPT), '--target', str(target), '--merge-entry']
            preview = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertFalse((target / 'scripts').exists())
            for directory in ('tests/', 'evidence/evals/'):
                self.assertNotIn('CREATE ' + directory, preview.stdout)
            result = subprocess.run(args + ['--apply'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(entry.read_text().startswith('# Existing user rules\n'))
            for directory in ('tests', 'evidence/evals'):
                self.assertFalse((target / directory).exists())
            self.assertTrue((target / 'evidence/methods/verify.md').is_file())
            self.assertTrue((target / 'evidence/testing/README.md').is_file())
            self.assertTrue((target / 'scripts/test_gate.py').is_file())
            self.assertFalse((target / '.github/workflows/harness-tests.yml').exists())
            original = entry.read_text()
            result = subprocess.run(args + ['--apply'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(entry.read_text(), original)
            check = subprocess.run([sys.executable, str(target / 'scripts/pm.py'), 'doctor'], capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stderr)

    def test_conflicts_reject_before_any_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / 'README.md').write_text('用户原有内容')
            result = subprocess.run([sys.executable, str(SCRIPT), '--target', tmp, '--apply'], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((target / 'README.md').read_text(), '用户原有内容')
            self.assertFalse((target / 'agent.md').exists())
