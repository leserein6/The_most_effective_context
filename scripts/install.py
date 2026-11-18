#!/usr/bin/env python3
"""Preview or install this workspace without overwriting existing user files."""
import argparse
from pathlib import Path
import shutil
import sys
import tempfile

START = b'\n<!-- project-workspace:start -->\n'
END = b'\n<!-- project-workspace:end -->\n'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target', required=True)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--merge-entry', action='store_true')
    a = p.parse_args()
    source = Path(__file__).resolve().parents[1]
    target = Path(a.target).expanduser().resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError('Source and target must be separate directory trees')
    plan = []
    conflicts = []
    for f in sorted(source.rglob('*')):
        rel = f.relative_to(source)
        if rel.parts[0] == 'tests' or rel.parts[:2] == ('evidence', 'evals'):
            continue
        if any(part in ('.pm-runtime', '__pycache__', '.git') for part in rel.parts) or f.suffix == '.pyc':
            continue
        if f.is_symlink():
            raise ValueError('Source symlink not supported: ' + str(rel))
        if not f.is_file():
            continue
        dest = target / rel
        for parent in (dest,) + tuple(dest.parents):
            if parent.is_symlink():
                raise ValueError('Target symlink not supported: ' + str(parent))
            if parent == target:
                break
        data = f.read_bytes()
        if dest.exists():
            if not dest.is_file():
                conflicts.append(str(rel)); continue
            original = dest.read_bytes()
            if original == data:
                continue
            block = START + data + END
            if rel.as_posix() == 'agent.md' and a.merge_entry:
                if block in original:
                    continue
                if START in original:
                    conflicts.append(str(rel) + ' (existing managed block differs)'); continue
                plan.append((f, dest, original + block, original))
            else:
                conflicts.append(str(rel))
        else:
            # An existing file in a parent position is also a preflight conflict.
            if any(parent.exists() and not parent.is_dir() for parent in dest.parents):
                conflicts.append(str(rel) + ' (parent is not a directory)'); continue
            plan.append((f, dest, data, None))
    if conflicts:
        raise ValueError('Refusing to overwrite existing paths: ' + ', '.join(conflicts))
    print(('APPLY' if a.apply else 'PREVIEW') + ': ' + str(target))
    for _, dest, _, old in plan:
        print(('MERGE ' if old is not None else 'CREATE ') + str(dest.relative_to(target)))
    if not a.apply:
        print('No files changed. Add --apply to install this exact plan.')
        return
    written = []
    try:
        for source_file, dest, data, old in plan:
            dest.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=dest.parent, delete=False) as f:
                temp = Path(f.name)
                f.write(data)
            try:
                shutil.copymode(dest if old is not None else source_file, temp)
                temp.replace(dest)
            finally:
                if temp.exists():
                    temp.unlink()
            written.append((dest, old))
    except BaseException:
        for dest, old in reversed(written):
            if old is None:
                dest.unlink()
            else:
                dest.write_bytes(old)
        raise
    print('Installed. Run python3 scripts/pm.py doctor in the target directory.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as e:
        print('ERROR: ' + str(e), file=sys.stderr)
        sys.exit(2)
