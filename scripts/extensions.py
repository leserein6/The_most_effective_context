#!/usr/bin/env python3
"""Discover declarative Markdown method packages within a Harness root."""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TASKS = ('answer', 'proposal', 'change', 'assess', 'learn')
ID = re.compile(r'[a-z][a-z0-9-]*')
FILE = re.compile(r'(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_-]+[.]md')


def packages(root):
    directory = root / 'extensions'
    if directory.is_symlink():
        raise ValueError('Symlink extension root: ' + str(directory))
    if not directory.exists():
        return
    for package in sorted(directory.iterdir()):
        descriptor = package / 'extension.json'
        if package.is_symlink() or descriptor.is_symlink() or descriptor.exists():
            yield package


def read_package(package):
    if package.is_symlink():
        raise ValueError('Symlink extension package: ' + str(package))
    descriptor = package / 'extension.json'
    if descriptor.is_symlink() or not descriptor.is_file():
        raise ValueError('Expected a regular extension.json')
    spec = json.loads(descriptor.read_text(encoding='utf-8'))
    if not isinstance(spec, dict) or type(spec.get('schema_version')) is not int or spec['schema_version'] != 1:
        raise ValueError('Expected method extension schema version 1')
    if not ID.fullmatch(package.name) or spec.get('id') != package.name:
        raise ValueError('Extension ID must match its directory')
    for key in ('when', 'output'):
        if not isinstance(spec.get(key), str) or not spec[key].strip():
            raise ValueError('Missing extension field: ' + key)
    tasks = spec.get('tasks')
    if not isinstance(tasks, list) or not tasks or any(t not in TASKS for t in tasks):
        raise ValueError('Expected a nonempty list of known Task types')
    if not isinstance(spec.get('resources'), list):
        raise ValueError('Expected a list of Markdown resources')
    seen = set()
    for name in [spec.get('entry')] + spec['resources']:
        if not isinstance(name, str) or not FILE.fullmatch(name) or name in seen:
            raise ValueError('Invalid or duplicate Markdown path: ' + repr(name))
        seen.add(name)
        path = package / name
        if path.resolve() != path or not path.is_file():
            raise ValueError('Missing or linked extension file: ' + str(path))
    return spec


def distribution_files(root):
    files = []
    for package in packages(root):
        try:
            spec = read_package(package)
        except (ValueError, OSError) as exc:
            raise ValueError('{}: {}'.format(package, exc)) from exc
        for name in ['extension.json', spec['entry']] + spec['resources']:
            files.append((package / name).relative_to(root).as_posix())
    return files


def disabled_marker(root, name):
    path = root / '.harness-local' / 'disabled' / name
    if path.resolve() != path or (path.exists() and not path.is_file()):
        raise ValueError('Invalid extension setting: ' + str(path))
    return path


def candidates(root, task):
    result = []
    for package in packages(root):
        try:
            if disabled_marker(root, package.name).exists():
                continue
            spec = read_package(package)
            if task and task not in spec['tasks']:
                continue
            summary = {k: spec[k] for k in ('id', 'when', 'output')}
            summary['entry'] = (package / spec['entry']).relative_to(root).as_posix()
            result.append(summary)
        except (ValueError, OSError) as exc:
            print('Skipped {}: {}'.format(package.name, exc), file=sys.stderr)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('list').add_argument('--task', choices=TASKS)
    for action in ('enable', 'disable'):
        commands.add_parser(action).add_argument('id')
    args = parser.parse_args()
    if args.command == 'list':
        print(json.dumps(candidates(ROOT, args.task), ensure_ascii=False))
        return
    if not ID.fullmatch(args.id):
        raise ValueError('Invalid extension ID')
    package = ROOT / 'extensions' / args.id
    if package.resolve() != package or not (package / 'extension.json').is_file():
        raise ValueError('Unknown or linked extension: ' + args.id)
    marker = disabled_marker(ROOT, args.id)
    if args.command == 'disable':
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch(exist_ok=True)
    else:
        read_package(package)
        marker.unlink(missing_ok=True)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(2)
