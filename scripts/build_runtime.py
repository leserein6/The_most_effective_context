#!/usr/bin/env python3
"""Build a minimal, reproducible Harness install archive for end users.

Unlike git clone, the archive contains only install.py, its manifest, and the
runtime files enumerated by the core and method package manifests. It contains no
maintainer docs, tests, source Project instances, or Git metadata.
"""
import argparse
import hashlib
import stat
import sys
import zipfile
from pathlib import Path

from install import load_manifest, WORK_SOP_SKILLS, optional_skill_paths

BOOTSTRAP_FILES = ('install-manifest.json', 'scripts/install.py')
RESTRICTED_ROOTS = ('docs/', 'tests/', 'examples/', 'project-management/projects/', '.git/')


def runtime_paths(source):
    paths = sorted(set(load_manifest(source)) | set(BOOTSTRAP_FILES) | set(optional_skill_paths(WORK_SOP_SKILLS)))
    for rel in paths:
        if rel in ('README.md', '.gitignore') or rel.startswith(RESTRICTED_ROOTS):
            raise ValueError('Maintainer or user-state path in distribution: ' + rel)
        path = source / rel
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != source):
            raise ValueError('Symlink in distribution path: ' + rel)
        if not path.is_file():
            raise ValueError('Missing distribution file: ' + rel)
    return paths


def verify_archive(source, archive_path, paths):
    with zipfile.ZipFile(archive_path, 'r') as z:
        names = z.namelist()
        if len(names) != len(set(names)) or set(names) != set(paths):
            raise ValueError('Distribution does not match the install manifest')
        if z.testzip() is not None:
            raise ValueError('Invalid archive checksum')
        for rel in paths:
            if z.read(rel) != (source / rel).read_bytes():
                raise ValueError('Archive file differs from source: ' + rel)


def build(source, archive_path):
    paths = runtime_paths(source)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    if archive_path.is_symlink():
        raise ValueError('Refusing to replace symlink archive')
    with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in paths:
            path = source / rel
            meta = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            meta.create_system = 3
            meta.external_attr = ((stat.S_IFREG | (path.stat().st_mode & 0o777)) << 16)
            meta.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(meta, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    verify_archive(source, archive_path, paths)
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    (archive_path.parent / (archive_path.name + '.sha256')).write_text(
        '{}  {}\n'.format(digest, archive_path.name), encoding='ascii')
    print('Archive: {} ({} runtime, optional skill, and installer files)'.format(archive_path, len(paths)))
    print('SHA256: {}'.format(digest))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='dist/harness-runtime.zip',
                        help='output archive path (default: dist/harness-runtime.zip)')
    parser.add_argument('--verify', action='store_true',
                        help='verify an existing archive against the current manifest/source')
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    output = Path(args.output).expanduser().absolute()
    if args.verify:
        paths = runtime_paths(source)
        verify_archive(source, output, paths)
        print('Verified {} ({} files; no maintainer docs or source Project data)'.format(output, len(paths)))
    else:
        build(source, output)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(2)
