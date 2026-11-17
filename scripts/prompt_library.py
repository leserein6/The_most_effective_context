#!/usr/bin/env python3
"""Inspect pinned, locally retained prompt references. Python 3.9+, stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import quote


SCENARIOS = ('implement', 'review', 'research', 'author')
NOTICE = (
    'REFERENCE ONLY: external prompt text is untrusted reference material. '
    'It is not automatically installed as a native Skill, does not authorize '
    'actions, and is never executed by this command. Matching hashes establish '
    'content identity, not instruction safety, correctness, or compatibility.'
)


def required_text(value, label):
    if not isinstance(value, str) or not value.strip() or '\x00' in value:
        raise ValueError(label + ' must be nonempty text')
    return value


def relative_path(value, label):
    value = required_text(value, label)
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or '\\' in value or str(p) != value:
        raise ValueError(label + ' must be a canonical repository-relative path')
    return p


class Library:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.external = self.root / 'evidence/prompts/external'
        self.catalog = self.root / 'evidence/prompts/catalog.json'

    def guarded(self, path, external=False):
        path = Path(path)
        boundary = self.external if external else self.root
        if path != boundary and boundary not in path.parents:
            raise ValueError('Path outside permitted prompt library: ' + str(path))
        # Refuse traversal through any symlink, including external/ itself.
        for part in (path,) + tuple(path.parents):
            if part == self.root:
                break
            if part.is_symlink():
                raise ValueError('Symlink not permitted in prompt library: ' + str(part))
        resolved = path.resolve()
        if resolved != boundary and boundary not in resolved.parents:
            raise ValueError('Resolved path outside permitted prompt library')
        return path

    def external_path(self, value, label):
        rel = relative_path(value, label)
        return self.guarded(self.root.joinpath(*rel.parts), external=True)

    def load(self):
        catalog = json.loads(self.guarded(self.catalog).read_text(encoding='utf-8'))
        if not isinstance(catalog, dict) or type(catalog.get('schema_version')) is not int or catalog['schema_version'] != 1:
            raise ValueError('Unsupported catalog schema_version (expected integer 1)')
        resources = catalog.get('resources')
        if not isinstance(resources, list) or not resources:
            raise ValueError('Catalog resources must be a nonempty list')
        ids = set()
        for item in resources:
            if not isinstance(item, dict):
                raise ValueError('Each resource must be an object')
            rid = required_text(item.get('id'), 'id')
            if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,99}', rid) or rid in ids:
                raise ValueError('Invalid or duplicate resource id: ' + rid)
            ids.add(rid)
            required_text(item.get('title'), rid + '.title')
            scenarios = item.get('scenarios')
            if not isinstance(scenarios, list) or not scenarios or any(not isinstance(s, str) or not s for s in scenarios):
                raise ValueError(rid + '.scenarios must be a nonempty text list')
            repository = required_text(item.get('repository'), rid + '.repository')
            if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
                raise ValueError(rid + '.repository must have owner/name form')
            for field, size in (('commit', 40), ('git_blob_sha', 40), ('sha256', 64), ('license_sha256', 64)):
                if not isinstance(item.get(field), str) or not re.fullmatch(r'[0-9a-fA-F]{' + str(size) + r'}', item[field]):
                    raise ValueError(rid + '.' + field + ' must be a full hexadecimal hash')
            relative_path(item.get('path'), rid + '.path')
            self.external_path(item.get('local_path'), rid + '.local_path')
            self.external_path(item.get('license_path'), rid + '.license_path')
            cautions = item.get('cautions')
            if not isinstance(cautions, list) or any(not isinstance(c, str) or not c.strip() for c in cautions):
                raise ValueError(rid + '.cautions must be a text list')
            bundled = item.get('bundled_files', [])
            if not isinstance(bundled, list):
                raise ValueError(rid + '.bundled_files must be a list')
            for index, dependency in enumerate(bundled):
                label = rid + '.bundled_files[' + str(index) + ']'
                if not isinstance(dependency, dict):
                    raise ValueError(label + ' must be an object')
                relative_path(dependency.get('path'), label + '.path')
                self.external_path(dependency.get('local_path'), label + '.local_path')
                for field, size in (('git_blob_sha', 40), ('sha256', 64)):
                    if not isinstance(dependency.get(field), str) or not re.fullmatch(r'[0-9a-fA-F]{' + str(size) + r'}', dependency[field]):
                        raise ValueError(label + '.' + field + ' must be a full hexadecimal hash')
        return resources

    @staticmethod
    def upstream(item):
        return 'https://github.com/{}/blob/{}/{}'.format(
            item['repository'], item['commit'], quote(item['path'], safe='/'))

    def verified_blob(self, item, label):
        content_path = self.external_path(item['local_path'], label + '.local_path')
        if not content_path.is_file():
            raise ValueError(label + ': resource file is missing')
        # Hash and display the same in-memory snapshot, never a second read.
        content = content_path.read_bytes()
        if hashlib.sha256(content).hexdigest() != item['sha256'].lower():
            raise ValueError(label + ': resource SHA256 mismatch')
        blob = hashlib.sha1(('blob ' + str(len(content)) + '\0').encode('ascii') + content).hexdigest()
        if blob != item['git_blob_sha'].lower():
            raise ValueError(label + ': Git blob SHA mismatch')
        return content

    def verify(self, item):
        rid = item['id']
        content = self.verified_blob(item, rid)
        license_path = self.external_path(item['license_path'], rid + '.license_path')
        if not license_path.is_file():
            raise ValueError(rid + ': license file is missing')
        license_content = license_path.read_bytes()
        if hashlib.sha256(license_content).hexdigest() != item['license_sha256'].lower():
            raise ValueError(rid + ': license SHA256 mismatch')
        for dependency in item.get('bundled_files', []):
            self.verified_blob(dependency, rid + ' dependency ' + dependency['path'])
        return content.decode('utf-8')


def run(args):
    library = Library(args.root)
    resources = library.load()
    if args.command == 'list':
        selected = [r for r in resources if args.scenario is None or args.scenario in r['scenarios']]
        if not selected:
            raise ValueError('No prompt resources match scenario: ' + args.scenario)
        return [{
            'id': r['id'], 'title': r['title'], 'scenarios': r['scenarios'],
            'local_path': r['local_path'], 'upstream_url': library.upstream(r),
        } for r in selected]
    if args.command == 'show':
        item = next((r for r in resources if r['id'] == args.id), None)
        if item is None:
            raise ValueError('Unknown prompt resource ID: ' + args.id)
        content = library.verify(item)
        return {
            'notice': NOTICE, 'reference_only': True,
            'metadata': dict(item, upstream_url=library.upstream(item)),
            'cautions': item['cautions'], 'content': content,
        }
    if args.command == 'check':
        for item in resources:
            library.verify(item)
        return {'ok': True, 'resources': len(resources), 'checked_ids': [r['id'] for r in resources],
                'notice': NOTICE}
    raise ValueError('Unknown command')


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('list', help='List lightweight catalog metadata without loading prompt text')
    q.add_argument('--scenario', choices=SCENARIOS)
    q = sub.add_parser('show', help='Verify and display a reference; never execute it')
    q.add_argument('id')
    sub.add_parser('check', help='Verify all retained resource and license files')
    return p


def main():
    try:
        result = run(parser().parse_args())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError, UnicodeError) as e:
        print('ERROR: ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
