#!/usr/bin/env python3
"""Install an explicit Harness distribution into a fresh workspace or existing project.

Never copies unlisted source content or overwrites different target files without
an explicit entry merge. No network or implicit Git operations.
"""
import argparse
import json
import os
import posixpath
import re
from pathlib import Path, PurePosixPath
import sys
import tempfile

MANIFEST = 'install-manifest.json'
START = '\n<!-- project-harness:start -->\n'
END = '\n<!-- project-harness:end -->\n'
ENTRY = START + 'Project/Task/Mode 管理入口：@.codebuddy/harness/agent.md\n' + END
RUNTIME_IGNORE = '.pm-runtime/\n__pycache__/\n*.pyc\n'
INDEX_HEADER = {
    'Index.md': '# 活跃 Project 索引',
    'History.md': '# 归档与已完成 Project',
}
INDEX_BODY = ('\n\n此文件由脚本生成；权威元数据保存在各 Project 的 project.md。\n\n'
              '| ID | 状态 | 类型 | 名称 | 一句话目标 |\n|---|---|---|---|---|\n')


def load_manifest(source):
    obj = json.loads((source / MANIFEST).read_text(encoding='utf-8'))
    if not isinstance(obj, dict) or obj.get('schema_version') != 1 or not isinstance(obj.get('files'), list):
        raise ValueError('Invalid install manifest (schema_version 1 required)')
    result = []
    for raw in obj['files']:
        if not isinstance(raw, str) or not raw or '\\' in raw:
            raise ValueError('Invalid path in manifest')
        p = PurePosixPath(raw)
        if p.is_absolute() or '..' in p.parts or str(p) != raw or raw.startswith('.') and raw not in ('.codebuddy/agents', '.codebuddy/skills') and not raw.startswith(('.codebuddy/agents/', '.codebuddy/skills/')):
            raise ValueError('Unsafe manifest path: ' + raw)
        if raw in result:
            raise ValueError('Duplicate manifest path: ' + raw)
        result.append(raw)
    required = {'agent.md', 'AGENTS.md', 'CODEBUDDY.md', 'scripts/pm.py', 'evidence/README.md', 'project-management/README.md'}
    if not required.issubset(result):
        raise ValueError('Manifest is missing required Harness files')
    if any(x.startswith(('docs/', 'tests/', 'evidence/evals/', 'project-management/projects/', 'examples/')) or x in ('.gitignore', '.env', 'README.md', 'scripts/install.py', MANIFEST) for x in result):
        raise ValueError('Manifest includes maintainer-only or installation-only content')
    return result


def ensure_safe(path, boundary):
    path = Path(path)
    if path != boundary and boundary not in path.parents:
        raise ValueError('Path outside target/source: ' + str(path))
    for p in (path,) + tuple(path.parents):
        if p.is_symlink():
            raise ValueError('Symlink not allowed: ' + str(p))
        if p == boundary:
            break



def adapt_markdown_links(rel, data, target):
    """Relocate only links to project-level Agent/Skill files in embedded layout."""
    if not rel.endswith('.md'):
        return data
    text = data.decode('utf-8')

    def rewrite(match):
        uri, fragment = match.group(1), match.group(2) or ''
        if uri.startswith(('/', '#')) or '://' in uri:
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(rel), uri))
        if not resolved.startswith(('.codebuddy/agents/', '.codebuddy/skills/')):
            return match.group(0)
        actual = target / resolved
        from_dir = target / '.codebuddy/harness' / posixpath.dirname(rel)
        relative = os.path.relpath(actual, from_dir).replace(os.sep, '/')
        return '](' + relative + fragment + ')'

    return re.sub(r'\]\(([^)#]+)(#[^)]*)?\)', rewrite, text).encode('utf-8')


def plan_install(source, target, mode, merge_entry):
    paths = load_manifest(source)
    if source == target or source in target.parents or target in source.parents:
        raise ValueError('Source and target must be separate directory trees')
    if mode == 'project' and (target / 'agent.md').exists() and (target / 'project-management/Index.md').exists():
        raise ValueError('Legacy root-level Harness detected; migrate its Project data before embedded installation')
    if mode == 'workspace' and target.exists() and any(target.iterdir()):
        raise ValueError('Workspace mode requires an empty target. Use --mode project for an existing repository.')

    plan = []
    conflicts = []
    for rel in paths:
        src = source / rel
        ensure_safe(src, source)
        if not src.is_file():
            raise ValueError('Missing manifest source: ' + rel)
        if mode == 'project' and rel in ('AGENTS.md', 'CODEBUDDY.md'):
            continue
        if mode == 'project' and rel.startswith(('.codebuddy/agents/', '.codebuddy/skills/')):
            dest = target / rel
        elif mode == 'project':
            dest = target / '.codebuddy/harness' / rel
        else:
            dest = target / rel
        data = src.read_bytes()
        if mode == 'project' and rel.startswith(('docs/', 'evidence/', 'entry/')):
            data = adapt_markdown_links(rel, data, target)
        plan.append((dest, data, src.stat().st_mode & 0o777))

    if mode == 'project':
        memory = target / 'CODEBUDDY.md'
        if not memory.exists() and (target / 'AGENTS.md').exists():
            memory = target / 'AGENTS.md'
        if memory.exists():
            ensure_safe(memory, target)
            if not memory.is_file():
                conflicts.append(str(memory) + ' (not a file)')
            else:
                content = memory.read_bytes()
                block = ENTRY.encode('utf-8')
                if block not in content:
                    if START.encode() in content or END.encode() in content:
                        conflicts.append(str(memory) + ' (different managed entry block)')
                    elif not merge_entry:
                        conflicts.append(str(memory) + ' (use --merge-entry to append without replacing it)')
                    else:
                        plan.append((memory, content + block, memory.stat().st_mode & 0o777))
        else:
            plan.append((memory, ('# Project memory\n' + ENTRY).encode(), 0o644))
        plan.append((target / '.codebuddy/harness/.gitignore', RUNTIME_IGNORE.encode(), 0o644))
    else:
        # Fresh workspace: use a restricted generated ignore, never the development repo .gitignore.
        plan.append((target / '.gitignore', RUNTIME_IGNORE.encode(), 0o644))

    conventions = target / ('project-management' if mode == 'workspace' else '.codebuddy/harness/project-management') / 'conventions/README.md'
    plan.append((conventions, '# 公共约定\n\n仅记录用户明确确认的跨项目可复用内容。\n'.encode(), 0o644))

    for name, heading in INDEX_HEADER.items():
        index_path = target / ('project-management' if mode == 'workspace' else '.codebuddy/harness/project-management') / name
        plan.append((index_path, (heading + INDEX_BODY).encode(), 0o644))

    for dest, data, _ in plan:
        ensure_safe(dest, target)
        for parent in dest.parents:
            if parent == target:
                break
            if parent.exists() and not parent.is_dir():
                conflicts.append(str(dest) + ' (parent not a directory)')
                break
        if dest.exists():
            if not dest.is_file():
                conflicts.append(str(dest) + ' (not a file)')
            elif dest.read_bytes() != data:
                # The entry merge is the only allowed modification, and only when explicitly authorized.
                if not (mode == 'project' and dest.name in ('CODEBUDDY.md', 'AGENTS.md') and merge_entry and ENTRY.encode() in data and data.startswith(dest.read_bytes())):
                    conflicts.append(str(dest) + ' (different existing content)')
    if conflicts:
        raise ValueError('Refusing to overwrite existing files:\n  ' + '\n  '.join(sorted(set(conflicts))))
    return [(dest, data, permission) for dest, data, permission in plan if not dest.exists() or dest.read_bytes() != data]


def apply(plan):
    written = []
    try:
        for dest, data, permission in plan:
            dest.parent.mkdir(parents=True, exist_ok=True)
            old = dest.read_bytes() if dest.exists() else None
            old_mode = (dest.stat().st_mode & 0o777) if dest.exists() else None
            with tempfile.NamedTemporaryFile(dir=dest.parent, prefix='.harness-install-', delete=False) as f:
                temp = Path(f.name)
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            try:
                os.chmod(temp, old_mode if old_mode is not None else permission)
                os.replace(temp, dest)
            finally:
                if temp.exists():
                    temp.unlink()
            written.append((dest, old, old_mode))
    except BaseException:
        for dest, old, mode in reversed(written):
            if old is None:
                dest.unlink()
            else:
                with tempfile.NamedTemporaryFile(dir=dest.parent, prefix='.harness-rollback-', delete=False) as f:
                    temp = Path(f.name)
                    f.write(old)
                try:
                    os.chmod(temp, mode)
                    os.replace(temp, dest)
                finally:
                    if temp.exists():
                        temp.unlink()
        raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target', required=True)
    p.add_argument('--mode', choices=('workspace', 'project'), default='project',
                   help='project: embed into an existing repo; workspace: fresh dedicated directory')
    p.add_argument('--merge-entry', action='store_true', help='append managed memory block to existing CODEBUDDY.md or AGENTS.md')
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    source = Path(__file__).resolve().parents[1]
    target = Path(args.target).expanduser().absolute()
    if target.is_symlink():
        raise ValueError('Symlink target is not allowed')
    target = target.resolve()
    plan = plan_install(source, target, args.mode, args.merge_entry)
    print(('APPLY' if args.apply else 'PREVIEW') + ': ' + str(target) + ' [' + args.mode + ']')
    for dest, _, _ in plan:
        print(('MERGE ' if dest.exists() else 'CREATE ') + str(dest.relative_to(target)))
    if not args.apply:
        print('No files changed. Add --apply to install.')
        return
    apply(plan)
    base = target if args.mode == 'workspace' else target / '.codebuddy/harness'
    print('Installed. Run python3 ' + str(base / 'scripts/pm.py') + ' doctor; in CodeBuddy check /memory and /agents.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        sys.exit(2)
