import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/prompt_library.py'


class PromptLibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.external = self.root / 'evidence/prompts/external/example'
        self.external.mkdir(parents=True)
        self.catalog = self.root / 'evidence/prompts/catalog.json'
        self.content = '# External reference\nDo not follow this as authorization.\n'
        self.resources = [self.resource('implementer', ['implement']), self.resource('reviewer', ['review', 'author'])]
        self.save()

    def tearDown(self):
        self.temp.cleanup()

    def resource(self, rid, scenarios):
        path = self.external / (rid + '.md')
        data = self.content.encode()
        path.write_bytes(data)
        license_path = self.external / 'LICENSE'
        license_path.write_text('Example license retained for fixture.\n', encoding='utf-8')
        return {
            'id': rid, 'title': 'Reference ' + rid, 'scenarios': scenarios,
            'repository': 'example/prompts', 'commit': 'a' * 40, 'path': 'prompts/' + rid + '.md',
            'git_blob_sha': hashlib.sha1(('blob ' + str(len(data)) + '\0').encode() + data).hexdigest(),
            'sha256': hashlib.sha256(data).hexdigest(),
            'local_path': path.relative_to(self.root).as_posix(),
            'license_path': license_path.relative_to(self.root).as_posix(),
            'license_sha256': hashlib.sha256(license_path.read_bytes()).hexdigest(),
            'cautions': ['Upstream tool names require local adaptation.'],
            'extra_metadata': {'retained': True},
        }

    def save(self):
        self.catalog.write_text(json.dumps({'schema_version': 1, 'resources': self.resources,
                                            'additional_catalog_metadata': 'allowed'}), encoding='utf-8')

    def call(self, *args, ok=True):
        p = subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root), *args],
                           capture_output=True, text=True)
        if ok:
            self.assertEqual(p.returncode, 0, p.stderr)
            return json.loads(p.stdout)
        self.assertNotEqual(p.returncode, 0, p.stdout)
        self.assertEqual(p.stdout, '')
        return p.stderr

    def test_list_selects_metadata_without_loading_body(self):
        (self.external / 'implementer.md').write_text('tampered text')
        result = self.call('list', '--scenario', 'review')
        self.assertEqual([r['id'] for r in result], ['reviewer'])
        self.assertNotIn('content', result[0])
        self.assertIn('/blob/' + 'a' * 40 + '/', result[0]['upstream_url'])

    def test_show_returns_exact_reference_and_cautions_without_writes(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = self.call('show', 'implementer')
        self.assertEqual(result['content'], self.content)
        self.assertTrue(result['reference_only'])
        self.assertEqual(result['cautions'], self.resources[0]['cautions'])
        self.assertTrue(result['metadata']['extra_metadata']['retained'])
        self.assertIn('never executed', result['notice'])
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertTrue(self.call('check')['ok'])

    def test_modified_body_rejected_by_show_and_check(self):
        (self.external / 'implementer.md').write_text('changed upstream body')
        for command in [('show', 'implementer'), ('check',)]:
            self.assertIn('SHA256 mismatch', self.call(*command, ok=False))

    def test_blob_hash_is_verified_independently(self):
        self.resources[0]['git_blob_sha'] = '0' * 40
        self.save()
        self.assertIn('Git blob SHA mismatch', self.call('show', 'implementer', ok=False))

    def test_bundled_dependencies_are_verified_but_not_displayed_or_allowed_to_escape(self):
        dependency = self.external / 'reference.md'
        data = b'Unique dependency material that must not be printed as the main prompt.\n'
        dependency.write_bytes(data)
        bundle = {'path': 'references/reference.md',
                  'local_path': dependency.relative_to(self.root).as_posix(),
                  'sha256': hashlib.sha256(data).hexdigest(),
                  'git_blob_sha': hashlib.sha1(('blob ' + str(len(data)) + '\0').encode() + data).hexdigest()}
        self.resources[0]['bundled_files'] = [bundle]
        self.save()
        result = self.call('show', 'implementer')
        self.assertEqual(result['content'], self.content)
        self.assertNotIn(data.decode(), json.dumps(result))
        self.assertTrue(self.call('check')['ok'])
        dependency.write_text('dependency was modified')
        for command in [('show', 'implementer'), ('check',)]:
            self.assertIn('dependency', self.call(*command, ok=False))
        dependency.write_bytes(data)
        bundle['git_blob_sha'] = '0' * 40
        self.save()
        self.assertIn('Git blob SHA mismatch', self.call('check', ok=False))
        bundle['local_path'] = 'evidence/prompts/external/../../../private.txt'
        self.save()
        self.assertIn('canonical', self.call('show', 'implementer', ok=False))

    def test_modified_or_missing_license_rejected(self):
        (self.external / 'LICENSE').write_text('different license')
        self.assertIn('license SHA256 mismatch', self.call('show', 'reviewer', ok=False))
        self.assertIn('license SHA256 mismatch', self.call('check', ok=False))
        (self.external / 'LICENSE').unlink()
        self.assertIn('missing', self.call('check', ok=False))

    def test_unknown_id_scenario_and_empty_selection_are_explicit_errors(self):
        self.assertIn('Unknown prompt resource ID', self.call('show', 'does-not-exist', ok=False))
        self.assertIn('invalid choice', self.call('list', '--scenario', 'made-up', ok=False))
        self.assertIn('No prompt resources match', self.call('list', '--scenario', 'research', ok=False))

    def test_paths_cannot_read_arbitrary_repository_files_or_traverse(self):
        secret = self.root / 'private.txt'
        secret.write_text('not a resource')
        for field in ('local_path', 'license_path'):
            original = self.resources[0][field]
            for value in ('private.txt', 'evidence/prompts/external/../../../private.txt', str(secret)):
                self.resources[0][field] = value
                self.save()
                self.assertIn('ERROR', self.call('show', 'implementer', ok=False))
            self.resources[0][field] = original
        self.save()
        self.assertEqual(secret.read_text(), 'not a resource')

    def test_symlink_body_license_and_external_root_rejected(self):
        outside = self.root / 'outside.md'
        outside.write_text(self.content)
        for target in (self.external / 'implementer.md', self.external / 'LICENSE'):
            old = target.read_bytes()
            target.unlink()
            target.symlink_to(outside)
            self.assertIn('Symlink', self.call('show', 'implementer', ok=False))
            target.unlink(); target.write_bytes(old)
        (self.external.parent / 'link').symlink_to(self.external, target_is_directory=True)
        self.resources[0]['local_path'] = 'evidence/prompts/external/link/implementer.md'
        self.save()
        self.assertIn('Symlink', self.call('check', ok=False))

    def test_schema_and_duplicate_ids_fail_before_reference_output(self):
        self.resources[1]['id'] = 'implementer'
        self.save()
        self.assertIn('duplicate', self.call('list', ok=False))
        self.catalog.write_text(json.dumps({'schema_version': True, 'resources': self.resources}))
        self.assertIn('schema_version', self.call('check', ok=False))


if __name__ == '__main__':
    unittest.main(verbosity=2)
