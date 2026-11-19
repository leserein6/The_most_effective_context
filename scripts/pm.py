#!/usr/bin/env python3
"""Markdown-backed Project management. Python 3.9+, macOS/Linux, stdlib only."""
import argparse
import base64
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time
import uuid

TYPES = ('development', 'learning', 'one_off')
STATES = ('active', 'archived', 'completed')
MODES = ('clarify', 'research', 'plan', 'execute', 'review', 'learn', 'orchestrate')
WI_STATES = ('pending', 'in_progress', 'blocked', 'in_review', 'completed')
WI_KEYS = {'id', 'title', 'status', 'depends_on', 'acceptance', 'evidence', 'blocker', 'next_action', 'created_at', 'updated_at'}
WI_UPDATE_KEYS = {'op', 'id', 'title', 'status', 'depends_on', 'acceptance', 'evidence', 'blocker', 'next_action'}
START = '# Project metadata\n\n```json\n'
END = '\n```\n'


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def dump(x):
    return json.dumps(x, ensure_ascii=False, indent=2) + '\n'


def atomic(path, data, mode=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if mode is None and path.exists():
        mode = path.stat().st_mode & 0o777
    fd, name = tempfile.mkstemp(prefix='.pm-write-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as f:
            if mode is not None:
                os.fchmod(f.fileno(), mode)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
        # Persist the rename as well as the file contents on POSIX filesystems.
        d = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(d)
        finally:
            os.close(d)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def text_field(x, label, single=False):
    if not isinstance(x, str) or not x.strip() or '\x00' in x:
        raise ValueError(label + ' must be nonempty text')
    if single and ('\n' in x or '\r' in x):
        raise ValueError(label + ' must be one line')
    return x.strip()


def safe_id(x):
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,79}', x):
        raise ValueError('id must contain lowercase letters, digits, _ or - (1..80 chars)')
    return x


def md_meta(m):
    return START + dump(m).rstrip() + END


def read_meta(p):
    s = p.read_text(encoding='utf-8')
    if not s.startswith(START) or END not in s[len(START):]:
        raise ValueError('Invalid project metadata: ' + str(p))
    m = json.loads(s[len(START):].split(END, 1)[0])
    safe_id(m['id'])
    if m['type'] not in TYPES or m['status'] not in STATES:
        raise ValueError('Invalid type or status: ' + str(p))
    text_field(m['name'], 'name', True)
    text_field(m['summary'], 'summary', True)
    if p.parent.name != m['id'] or p.parent.parent.name != m['type'] or p.parent.parent.parent.name != m['status']:
        raise ValueError('Project metadata disagrees with directory: ' + str(p))
    return m


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.base = self.root / 'project-management'
        self.runtime = self.root / '.pm-runtime'
        self.journal = self.runtime / 'pending.json'

    def guarded(self, p):
        p = Path(p)
        if '..' in p.parts or not p.is_absolute():
            raise ValueError('Noncanonical path rejected')
        # Refuse symlink traversal: moving a project must never follow an external tree.
        if p != self.root and self.root not in p.parents:
            raise ValueError('Path outside workspace')
        for part in (p,) + tuple(p.parents):
            if part == self.root:
                break
            if part.is_symlink():
                raise ValueError('Symlink not supported in managed paths: ' + str(part))
        return p

    @contextlib.contextmanager
    def lock(self, recovery=False):
        self.guarded(self.runtime)
        self.runtime.mkdir(parents=True, exist_ok=True)
        with self.guarded(self.runtime / 'lock').open('a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            if self.journal.exists() and not recovery:
                raise ValueError('Interrupted transaction; run: pm.py recover --rollback')
            yield

    def projects(self):
        self.guarded(self.base)
        found = []
        seen = set()
        for state in STATES:
            for typ in TYPES:
                d = self.guarded(self.base / 'projects' / state / typ)
                if not d.exists():
                    continue
                for p in sorted(d.glob('*/project.md')):
                    self.guarded(p)
                    m = read_meta(p)
                    if m['id'] in seen:
                        raise ValueError('Duplicate project ID: ' + m['id'])
                    seen.add(m['id'])
                    found.append((p.parent, m))
        return found

    def get(self, pid):
        safe_id(pid)
        hits = [(p, m) for p, m in self.projects() if m['id'] == pid]
        if len(hits) != 1:
            raise ValueError('Project not found: ' + pid)
        return hits[0]

    def token(self, path):
        h = hashlib.sha256()
        # Shared state only. Work artifacts use separate file ownership/worktrees.
        for p in sorted(path.rglob('*')):
            self.guarded(p)
            rel = p.relative_to(path).as_posix()
            # Archived logs are immutable provenance checked by doctor, not per-turn mutable state.
            # Exclude their potentially large contents from optimistic-lock tokens.
            if rel.startswith('logs/archive/'):
                continue
            if (rel.startswith('work/') or rel.startswith('source/')) and rel != 'source/INDEX.md':
                continue
            if p.is_file():
                h.update(str(p.relative_to(path)).encode())
                h.update(b'\x00')
                h.update(hashlib.sha256(p.read_bytes()).digest())
        return h.hexdigest()

    def check(self, path, expected):
        if self.token(path) != expected:
            raise ValueError('CONFLICT: project changed; resume again, compare and merge before retrying')

    def indexes(self, tx):
        projects = self.projects()
        def esc(x):
            return x.replace('|', '\\|').replace('[', '\\[').replace(']', '\\]')
        for filename, states in [('Index.md', ('active',)), ('History.md', ('archived', 'completed'))]:
            lines = ['# ' + ('活跃 Project 索引' if filename == 'Index.md' else '归档与已完成 Project'), '',
                     '此文件由脚本生成；权威元数据保存在各 Project 的 project.md。', '',
                     '| ID | 状态 | 类型 | 名称 | 一句话目标 |', '|---|---|---|---|---|']
            for p, m in projects:
                if m['status'] in states:
                    link = p.relative_to(self.base).as_posix() + '/project.md'
                    lines.append('| {} | {} | {} | [{}]({}) | {} |'.format(
                        m['id'], m['status'], m['type'], esc(m['name']), link, esc(m['summary'])))
            tx.write(self.base / filename, '\n'.join(lines) + '\n')


class Transaction:
    def __init__(self, store):
        self.s = store
        self.before = {}

    def write(self, p, data, mode=None):
        p = self.s.guarded(p)
        key = str(p.relative_to(self.s.root))
        if key not in self.before:
            self.before[key] = {'data': base64.b64encode(p.read_bytes()).decode(), 'mode': p.stat().st_mode & 0o777} if p.exists() else None
            atomic(self.s.journal, dump({'before': self.before}).encode())
        if data is None:
            if p.exists():
                p.unlink()
        else:
            atomic(p, data.encode() if isinstance(data, str) else data, mode=mode)

    def __enter__(self):
        return self

    def __exit__(self, typ, val, tb):
        if typ:
            rollback(self.s)
        elif self.s.journal.exists():
            self.s.journal.unlink()
        return False


def rollback(s):
    if not s.journal.exists():
        return
    changes = json.loads(s.journal.read_text())['before']
    # Validate the complete journal before modifying anything.
    for rel in changes:
        if Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise ValueError('Invalid recovery path')
        s.guarded(s.root / rel)
        if not rel.startswith('project-management/'):
            raise ValueError('Invalid recovery path')
    for rel, old in reversed(list(changes.items())):
        p = s.root / rel
        if old is None:
            if p.exists():
                p.unlink()
        else:
            atomic(p, base64.b64decode(old['data']), mode=old['mode'])
    s.journal.unlink()


def read_payload(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Payload must be an object')
    return data


def append(tx, p, s):
    tx.write(p, (p.read_text(encoding='utf-8') if p.exists() else '') + s)


def bump(tx, path, meta):
    meta = dict(meta, revision=meta['revision'] + 1, updated_at=now())
    tx.write(path / 'project.md', md_meta(meta))
    return meta


def log_entry(mode, operations, evidence, outcome, turn, work_item_ids=None):
    return '\n## {} | {} | {}\n\n操作流水：\n{}\n\n证据：\n{}\n\n结果：{}\n'.format(
        now(), turn, mode, '\n'.join('- ' + x for x in operations),
        '\n'.join('- [{}] {} — {}'.format(e['kind'], e['claim'], e['source']) for e in evidence) or '- 未提供',
        outcome + ('\n关联工作项：' + ', '.join(work_item_ids) if work_item_ids else ''))



def work_item_id(value):
    if not isinstance(value, str) or not re.fullmatch(r'WI-[0-9]{2,5}', value):
        raise ValueError('Work Item ID must be WI-01 .. WI-99999')
    return value


def checked_text_list(value, label, required=False):
    if not isinstance(value, list) or (required and not value):
        raise ValueError(label + ' must be a nonempty list' if required else label + ' must be a list')
    return [text_field(v, label) for v in value]


def checked_evidence(value):
    if not isinstance(value, list):
        raise ValueError('Work Item evidence must be a list')
    for proof in value:
        if not isinstance(proof, dict) or set(proof) != {'kind', 'claim', 'source'}:
            raise ValueError('Work Item evidence requires kind, claim and source')
        if proof['kind'] not in ('observed', 'cited', 'inferred', 'unverified'):
            raise ValueError('Unknown Work Item evidence kind')
        text_field(proof['claim'], 'evidence claim')
        text_field(proof['source'], 'evidence source')
    return value


def validate_work_items(doc):
    if not isinstance(doc, dict) or set(doc) != {'schema_version', 'items'} or doc['schema_version'] != 1:
        raise ValueError('Invalid Work Item document schema')
    if not isinstance(doc['items'], list):
        raise ValueError('Work Items must be a list')
    by_id = {}
    for item in doc['items']:
        if not isinstance(item, dict) or set(item) != WI_KEYS:
            raise ValueError('Invalid Work Item fields')
        wid = work_item_id(item['id'])
        if wid in by_id:
            raise ValueError('Duplicate Work Item: ' + wid)
        by_id[wid] = item
        text_field(item['title'], 'Work Item title', True)
        if item['status'] not in WI_STATES:
            raise ValueError('Invalid Work Item status: ' + wid)
        checked_text_list(item['acceptance'], 'acceptance', required=True)
        checked_evidence(item['evidence'])
        deps = item['depends_on']
        if not isinstance(deps, list) or any(not isinstance(v, str) for v in deps):
            raise ValueError('Invalid Work Item dependencies: ' + wid)
        for dep in deps:
            work_item_id(dep)
        if len(set(deps)) != len(deps) or wid in deps:
            raise ValueError('Repeated/self dependency: ' + wid)
        if item['blocker'] is not None:
            text_field(item['blocker'], 'blocker')
        if item['next_action'] is not None:
            text_field(item['next_action'], 'next_action')
        if not isinstance(item['created_at'], str) or not isinstance(item['updated_at'], str):
            raise ValueError('Missing Work Item timestamps')
        if item['status'] == 'blocked' and not item['blocker']:
            raise ValueError('Blocked Work Item requires blocker: ' + wid)
        if item['status'] != 'blocked' and item['blocker'] is not None:
            raise ValueError('Stale blocker on non-blocked Work Item: ' + wid)
        if item['status'] == 'completed':
            if not any(p['kind'] == 'observed' for p in item['evidence']):
                raise ValueError('Completed Work Item requires observed evidence: ' + wid)
            if item['next_action'] is not None:
                raise ValueError('Completed Work Item cannot have next_action: ' + wid)
    for wid, item in by_id.items():
        for dep in item['depends_on']:
            if dep not in by_id:
                raise ValueError('Unknown Work Item dependency: ' + wid + ' -> ' + dep)
            if item['status'] in ('in_progress', 'in_review', 'completed') and by_id[dep]['status'] != 'completed':
                raise ValueError('Unfinished dependency blocks Work Item: ' + wid + ' -> ' + dep)
    visited = set()
    visiting = set()

    def visit(wid):
        if wid in visiting:
            raise ValueError('Work Item dependency cycle: ' + wid)
        if wid in visited:
            return
        visiting.add(wid)
        for dep in by_id[wid]['depends_on']:
            visit(dep)
        visiting.remove(wid)
        visited.add(wid)

    for wid in by_id:
        visit(wid)
    return doc


def read_work_items(path):
    if not path.exists():
        return None  # Existing Projects predate Work Items; migrate lazily.
    content = path.read_text(encoding='utf-8')
    prefix = '# Project Work Items\n\n' + chr(96) * 3 + 'json\n'
    suffix = '\n' + chr(96) * 3
    if not content.startswith(prefix) or suffix not in content[len(prefix):]:
        raise ValueError('Invalid work-items.md format: ' + str(path))
    data, tail = content[len(prefix):].split(suffix, 1)
    if tail.strip():
        raise ValueError('Unexpected text after Work Item data')
    return validate_work_items(json.loads(data))


def encode_work_items(doc):
    validate_work_items(doc)
    return '# Project Work Items\n\n' + chr(96) * 3 + 'json\n' + dump(doc).rstrip() + '\n' + chr(96) * 3 + '\n'


def updated_work_items(current, updates):
    if not isinstance(updates, list):
        raise ValueError('work_item_updates must be a list')
    document = {'schema_version': 1, 'items': [dict(v) for v in (current or {'items': []})['items']]}
    if not updates:
        return document
    by_id = {v['id']: v for v in document['items']}
    changed_ids = set()
    for change in updates:
        if not isinstance(change, dict) or set(change) - WI_UPDATE_KEYS:
            raise ValueError('Invalid Work Item update fields')
        op = change.get('op')
        wid = work_item_id(change.get('id'))
        if wid in changed_ids:
            raise ValueError('Work Item updated twice in one checkpoint: ' + wid)
        changed_ids.add(wid)
        if op == 'create':
            if wid in by_id:
                raise ValueError('Work Item already exists: ' + wid)
            stamp = now()
            entry = {
                'id': wid,
                'title': text_field(change.get('title'), 'title', True),
                'status': change.get('status', 'pending'),
                'depends_on': change.get('depends_on', []),
                'acceptance': change.get('acceptance'),
                'evidence': change.get('evidence', []),
                'blocker': change.get('blocker'),
                'next_action': change.get('next_action'),
                'created_at': stamp, 'updated_at': stamp,
            }
            document['items'].append(entry)
            by_id[wid] = entry
        elif op == 'update':
            if wid not in by_id:
                raise ValueError('Unknown Work Item: ' + wid)
            if not (set(change) - {'op', 'id'}):
                raise ValueError('Work Item update has no changes: ' + wid)
            entry = by_id[wid]
            previous_status = entry['status']
            for key in WI_UPDATE_KEYS - {'op', 'id', 'evidence'}:
                if key in change:
                    entry[key] = change[key]
            if 'evidence' in change:
                checked_evidence(change['evidence'])
                entry['evidence'] = entry['evidence'] + change['evidence']
            if entry['status'] == 'completed' and previous_status != 'completed':
                if not any(p['kind'] == 'observed' for p in change.get('evidence', [])):
                    raise ValueError('Completion transition needs new observed evidence: ' + wid)
            if entry['status'] != 'blocked' and 'blocker' not in change:
                entry['blocker'] = None
            if entry['status'] == 'completed' and 'next_action' not in change:
                entry['next_action'] = None
            entry['updated_at'] = now()
        else:
            raise ValueError('Work Item operation must be create or update')
    return validate_work_items(document)


def work_item_overview(doc):
    if doc is None:
        return {'tracked': False, 'counts': {}, 'items': [],
                'note': 'No structured Work Item plan yet; do not infer zero outstanding work'}
    items = doc['items']
    counts = {status: sum(item['status'] == status for item in items) for status in WI_STATES}
    unfinished = [v for v in items if v['status'] != 'completed']
    completed = [v for v in items if v['status'] == 'completed'][-10:]
    view = unfinished + completed
    return {'tracked': True, 'counts': counts,
            'items': [{'id': v['id'], 'title': v['title'], 'status': v['status'],
                       'depends_on': v['depends_on'], 'acceptance': v['acceptance'],
                       'blocker': v['blocker'], 'next_action': v['next_action'],
                       'latest_evidence': v['evidence'][-1:] } for v in view[:50]],
            'truncated': len(view) > 50,
            'file': 'work-items.md'}


def checkpoint(s, a):
    p, m = s.get(a.id)
    s.check(p, a.expected)
    d = read_payload(a.payload)
    unknown = set(d) - {'turn_id', 'mode', 'progress', 'next', 'open_questions', 'operations', 'evidence', 'outcome', 'decisions', 'notes', 'candidates', 'phase_end', 'work_item_ids', 'work_item_updates'}
    if unknown:
        raise ValueError('Unknown fields: ' + ', '.join(sorted(unknown)))
    turn = safe_id(d['turn_id'])
    if 'phase_end' in d and not isinstance(d['phase_end'], bool):
        raise ValueError('phase_end must be boolean')
    receipts = p / 'logs' / 'receipts.md'
    receipt_text = receipts.read_text() if receipts.exists() else ''
    if ('\n- ' + turn + '\n') in receipt_text:
        raise ValueError('Duplicate turn_id: ' + turn)
    if d['mode'] not in MODES:
        raise ValueError('Invalid mode')
    for key in ('progress', 'next', 'outcome'):
        text_field(d[key], key)
    for key in ('operations', 'open_questions', 'notes', 'candidates'):
        if key in d and (not isinstance(d[key], list) or any(not isinstance(v, str) or not v.strip() for v in d[key])):
            raise ValueError(key + ' must be a text list')
    if not d.get('operations'):
        raise ValueError('operations must record meaningful activity')
    if not isinstance(d.get('evidence'), list):
        raise ValueError('evidence must be a list (may be empty)')
    for e in d['evidence']:
        if not isinstance(e, dict):
            raise ValueError('evidence entries must be objects')
        if e['kind'] not in ('observed', 'cited', 'inferred', 'unverified'):
            raise ValueError('Invalid evidence kind')
        text_field(e['claim'], 'claim')
        text_field(e['source'], 'source')
    decisions = d.get('decisions', [])
    if not isinstance(decisions, list):
        raise ValueError('decisions must be a list')
    for decision in decisions:
        if not isinstance(decision, dict):
            raise ValueError('decisions entries must be objects')
        if decision.get('status') not in ('proposed', 'confirmed', 'superseded'):
            raise ValueError('Invalid decision status')
        text_field(decision['text'], 'decision')
        if decision['status'] != 'proposed':
            text_field(decision.get('user_evidence'), 'user_evidence')
    updates = d.get('work_item_updates', [])
    wi_path = p / 'work-items.md'
    existing_wi = read_work_items(wi_path)
    planned_wi = updated_work_items(existing_wi, updates)
    refs = d.get('work_item_ids', [])
    if not isinstance(refs, list) or any(not isinstance(v, str) for v in refs):
        raise ValueError('work_item_ids must be a list')
    if len(set(refs)) != len(refs):
        raise ValueError('Duplicate work_item_ids')
    known = {item['id'] for item in planned_wi['items']}
    if any(work_item_id(wid) not in known for wid in refs):
        raise ValueError('Turn Task references unknown Work Item')
    refs = sorted(set(refs) | {v['id'] for v in updates})
    with Transaction(s) as tx:
        if updates:
            tx.write(wi_path, encode_work_items(planned_wi))
        tx.write(p / 'state.md', '# 当前状态\n\n## 进度\n' + d['progress'] + '\n\n## 未解决问题\n' +
                 '\n'.join('- ' + x for x in d.get('open_questions', [])) + '\n\n## 下一步\n' + d['next'] + '\n')
        for key, filename in [('notes', 'notes.md'), ('candidates', 'knowledge-candidates.md')]:
            if d.get(key):
                append(tx, p / filename, '\n## ' + now() + '\n' + '\n'.join('- ' + x for x in d[key]) + '\n')
        for decision in decisions:
            append(tx, p / 'decisions.md', '\n- [{}] {}\n  用户依据：{}\n'.format(
                decision['status'], decision['text'], decision.get('user_evidence', '待确认')))
        append(tx, p / 'logs/current.md', log_entry(d['mode'], d['operations'], d['evidence'], d['outcome'], turn, refs))
        append(tx, receipts, '\n- ' + turn + '\n')
        if d.get('phase_end'):
            tx.write(p / 'logs/compression-due.md', '阶段结束：请评估并生成有来源的摘要，再执行 compact。\n')
        bump(tx, p, m)
        s.indexes(tx)
    payload = Path(a.payload).resolve()
    try:
        payload.relative_to(s.runtime.resolve())
    except ValueError:
        pass
    else:
        payload.unlink(missing_ok=True)
    return {'id': a.id, 'token': s.token(p), 'compression_due': compression_due(p), 'work_item_ids': refs}


def compression_due(p):
    current = p / 'logs/current.md'
    return (current.exists() and current.stat().st_size >= 32768) or (p / 'logs/compression-due.md').exists()


RUNTIME_TTL_SECONDS = 24 * 3600
RUNTIME_MAX_BYTES = 10 * 1024 * 1024


def runtime_bytes(path):
    total = 0
    for p in path.rglob('*'):
        try:
            if p.is_file() and not p.is_symlink():
                total += p.stat().st_size
        except OSError:
            pass
    return total


def sweep_runtime(s):
    """Drop expired scratch from .pm-runtime; lock and rollback payload stay."""
    runtime = s.runtime
    if not runtime.is_dir():
        return
    keep = {'lock', 'pending.json'}
    now = time.time()

    def drop(entry):
        try:
            if entry.is_symlink() or entry.is_file():
                entry.unlink()
            else:
                shutil.rmtree(entry)
        except OSError:
            pass

    for entry in list(runtime.iterdir()):
        if entry.name in keep:
            continue
        try:
            if now - entry.stat().st_mtime > RUNTIME_TTL_SECONDS:
                drop(entry)
        except OSError:
            pass
    if runtime_bytes(runtime) <= RUNTIME_MAX_BYTES:
        return
    entries = [e for e in runtime.iterdir() if e.name not in keep]
    entries.sort(key=lambda e: e.stat().st_mtime if e.exists() else 0)
    for entry in entries:
        if runtime_bytes(runtime) <= RUNTIME_MAX_BYTES:
            break
        drop(entry)


def run(a):
    s = Store(a.root)
    with s.lock(recovery=a.command == 'recover'):
        sweep_runtime(s)
        if a.command == 'init':
            with Transaction(s) as tx:
                s.indexes(tx)
            return {'initialized': str(s.root)}
        if a.command == 'index':
            return (s.base / ('History.md' if a.history else 'Index.md')).read_text(encoding='utf-8')
        if a.command == 'list':
            return [m for p, m in s.projects() if a.all or m['status'] == 'active']
        if a.command == 'create':
            if not a.confirmed:
                raise ValueError('User confirmation required: present name/type/summary first')
            safe_id(a.id)
            if any(m['id'] == a.id for p, m in s.projects()):
                raise ValueError('Project ID already exists')
            p = s.base / 'projects/active' / a.type / a.id
            if p.exists() and any(p.iterdir()):
                raise ValueError('Target directory not empty')
            m = {'schema_version': '1.0', 'id': a.id, 'name': text_field(a.name, 'name', True), 'type': a.type,
                 'summary': text_field(a.summary, 'summary', True), 'status': 'active',
                 'revision': 1, 'created_at': now(), 'updated_at': now()}
            with Transaction(s) as tx:
                tx.write(p / 'project.md', md_meta(m))
                for name, body in {
                    'definition.md': '# 项目定义\n\n## 要解决的问题\n待明确，不能根据方案虚构痛点。\n\n## 期望结果\n' + m['summary'] + '\n\n## 范围与交付物\n待明确。\n\n## 硬约束\n待明确。\n',
                    'state.md': '# 当前状态\n\n## 进度\n已建立项目，尚未执行。\n\n## 未解决问题\n待明确验收条件。\n\n## 下一步\n明确目标边界和验收条件。\n',
                    'acceptance.md': '# 验收条件\n\n尚未制定，不得宣称已完成。\n',
                    'decisions.md': '# 决策记录\n', 'notes.md': '# 项目知识\n',
                    'knowledge-candidates.md': '# 待确认的公共积累候选\n',
                    'source/INDEX.md': '# 资料索引\n\n按需补充：标题、来源、用途、更新时间。\n',
                    'work/README.md': '# 工作产物\n\n源码、报告、实验记录存放于此，或在此登记外部仓库路径。\n',
                    'logs/current.md': '# 当前操作日志\n',
                    'logs/summary.md': '# 历史摘要\n',
                    'logs/receipts.md': '# 已记录交互 ID\n',
                }.items():
                    tx.write(p / name, body)
                s.indexes(tx)
            return dict(m, path=str(p), token=s.token(p))
        if a.command == 'resume':
            p, m = s.get(a.id)
            files = {}
            for name in ('project.md', 'definition.md', 'state.md', 'acceptance.md', 'decisions.md', 'logs/summary.md', 'source/INDEX.md'):
                f = s.guarded(p / name)
                content = f.read_text(encoding='utf-8')
                files[name] = content[:12000]
                if len(content) > 12000:
                    files[name] += '\n[截断；需要时读取原文件剩余部分]\n'
            return {'path': str(p), 'token': s.token(p), 'files': files,
                    'work_items': work_item_overview(read_work_items(p / 'work-items.md')),
                    'compression_due': compression_due(p),
                    'read_on_demand': ['notes.md', 'logs/current.md', 'logs/archive/', 'source/', 'work/']}
        if a.command == 'work-items':
            p, m = s.get(a.id)
            return work_item_overview(read_work_items(p / 'work-items.md'))
        if a.command == 'checkpoint':
            return checkpoint(s, a)
        if a.command == 'describe':
            p, m = s.get(a.id)
            s.check(p, a.expected)
            if not a.name and not a.summary:
                raise ValueError('Provide --name or --summary')
            old = dict(m)
            if a.name:
                m['name'] = text_field(a.name, 'name', True)
            if a.summary:
                m['summary'] = text_field(a.summary, 'summary', True)
            with Transaction(s) as tx:
                bump(tx, p, m)
                append(tx, p / 'logs/current.md', '\n## {} | describe\n名称：{} -> {}\n目标：{} -> {}\n依据：{}\n'.format(
                    now(), old['name'], m['name'], old['summary'], m['summary'], text_field(a.reason, 'reason')))
                s.indexes(tx)
            return {'token': s.token(p)}
        if a.command == 'edit':
            p, m = s.get(a.id)
            s.check(p, a.expected)
            # Semantic conflicts and user confirmation remain Agent responsibilities.
            target = a.document
            content = Path(a.file).read_text(encoding='utf-8')
            text_field(content, 'document')
            with Transaction(s) as tx:
                tx.write(p / target, content)
                append(tx, p / 'logs/current.md', '\n## {} | edit {}\n{}\n'.format(now(), target, text_field(a.reason, 'reason')))
                bump(tx, p, m)
                s.indexes(tx)
            return {'token': s.token(p)}
        if a.command == 'status':
            p, m = s.get(a.id)
            s.check(p, a.expected)
            if not a.confirmed:
                raise ValueError('Status changes require user confirmation')
            if a.status == m['status']:
                raise ValueError('Already in requested status')
            reason = text_field(a.reason, 'reason')
            dest = s.base / 'projects' / a.status / m['type'] / a.id
            s.guarded(dest)
            if dest.exists() and any(dest.iterdir()):
                raise ValueError('Destination is not empty')
            files = [f for f in sorted(p.rglob('*')) if f.is_file()]
            for f in p.rglob('*'):
                s.guarded(f)
            with Transaction(s) as tx:
                for f in files:
                    tx.write(dest / f.relative_to(p), f.read_bytes(), mode=f.stat().st_mode & 0o777)
                    tx.write(f, None)
                m['status'] = a.status
                bump(tx, dest, m)
                append(tx, dest / 'logs/current.md', '\n## {} | status -> {}\n用户确认依据：{}\n'.format(now(), a.status, reason))
                s.indexes(tx)
            # Empty shells are harmless; remove only empty directories, never user data.
            for d in sorted(p.rglob('*'), reverse=True):
                if d.is_dir():
                    try:
                        d.rmdir()
                    except OSError:
                        pass
            try:
                p.rmdir()
            except OSError:
                pass
            return {'path': str(dest), 'token': s.token(dest), 'status': a.status}
        if a.command == 'compact':
            p, m = s.get(a.id)
            s.check(p, a.expected)
            current = p / 'logs/current.md'
            content = current.read_bytes()
            if current.read_text().strip() == '# 当前操作日志':
                raise ValueError('No log entries to compact')
            summary = text_field(Path(a.summary_file).read_text(encoding='utf-8'), 'summary')
            for heading in ('## 已完成', '## 决策', '## 未解决', '## 恢复位置'):
                if heading not in summary:
                    raise ValueError('Summary requires heading: ' + heading)
            stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8]
            rel = 'logs/archive/' + stamp + '.md'
            digest = hashlib.sha256(content).hexdigest()
            with Transaction(s) as tx:
                tx.write(p / rel, content)
                append(tx, p / 'logs/summary.md', '\n# 压缩 {}\n\n原始日志：[{}]({})\n\nSHA256: {}\n\n{}\n'.format(
                    stamp, stamp, 'archive/' + stamp + '.md', digest, summary))
                tx.write(current, '# 当前操作日志\n')
                due = p / 'logs/compression-due.md'
                if due.exists():
                    tx.write(due, None)
                bump(tx, p, m)
                s.indexes(tx)
            return {'archive': rel, 'sha256': digest, 'token': s.token(p)}
        if a.command == 'promote':
            p, m = s.get(a.id)
            s.check(p, a.expected)
            if not a.confirmed:
                raise ValueError('Public conventions require user confirmation')
            title = text_field(a.title, 'title', True)
            body = text_field(Path(a.file).read_text(encoding='utf-8'), 'convention')
            user_evidence = text_field(a.reason, 'user confirmation evidence')
            with Transaction(s) as tx:
                append(tx, s.base / 'conventions/README.md', '\n## {}\n\n来源 Project：{}；确认依据：{}\n\n{}\n'.format(title, a.id, user_evidence, body))
                append(tx, p / 'logs/current.md', '\n## {} | promote\n公共积累：{}\n用户依据：{}\n'.format(now(), title, user_evidence))
                bump(tx, p, m)
                s.indexes(tx)
            return {'promoted': title, 'token': s.token(p)}
        if a.command == 'doctor':
            errors = []
            # Detect orphan project directories that projects() cannot discover.
            project_root = s.base / 'projects'
            if project_root.exists():
                s.guarded(project_root)
                for state_dir in sorted(project_root.iterdir()):
                    s.guarded(state_dir)
                    if state_dir.name not in STATES or not state_dir.is_dir():
                        errors.append('Unexpected project status directory: ' + str(state_dir))
                        continue
                    for type_dir in sorted(state_dir.iterdir()):
                        s.guarded(type_dir)
                        if type_dir.name not in TYPES or not type_dir.is_dir():
                            errors.append('Unexpected project type directory: ' + str(type_dir))
                            continue
                        for child in sorted(type_dir.iterdir()):
                            s.guarded(child)
                            if child.name == '.gitkeep':
                                continue
                            if not child.is_dir() or not (child / 'project.md').is_file():
                                errors.append('Incomplete project directory: ' + str(child))
            try:
                projects = s.projects()
            except (ValueError, KeyError, TypeError, OSError) as exc:
                errors.append('Project metadata invalid: ' + str(exc))
                projects = []
            for p, m in projects:
                try:
                    read_work_items(p / 'work-items.md')
                except (ValueError, KeyError, TypeError, OSError) as exc:
                    errors.append('Work Items invalid: ' + str(p) + ': ' + str(exc))
                for name in ('definition.md', 'state.md', 'acceptance.md', 'decisions.md', 'notes.md', 'source/INDEX.md', 'logs/current.md', 'logs/summary.md', 'logs/receipts.md'):
                    if not (p / name).is_file():
                        errors.append(str(p / name) + ' missing')
                for f in p.rglob('*'):
                    s.guarded(f)
                summary_file = p / 'logs/summary.md'
                summary = summary_file.read_text(encoding='utf-8') if summary_file.exists() else ''
                archive = p / 'logs/archive'
                references = re.findall(
                    r'原始日志：\[[^\]]+\]\(archive/([^/)\n]+\.md)\)\s*\n\s*SHA256:\s*([0-9a-f]{64})',
                    summary)
                # Missing/corrupted links must not silently evade hash checking.
                if (summary.count('原始日志：') != len(references)
                        or summary.count('SHA256:') != len(references)
                        or len({name for name, _ in references}) != len(references)):
                    errors.append('Malformed or duplicate archive references: ' + str(summary_file))
                listed = set()
                for fname, digest in references:
                    listed.add(fname)
                    if not re.fullmatch(r'[0-9]{8}T[0-9]{6}-[0-9a-f]{8}\.md', fname):
                        errors.append('Invalid archive filename: ' + fname)
                        continue
                    path = s.guarded(archive / fname)
                    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                        errors.append('Archive integrity failure: ' + str(path))
                if archive.exists():
                    s.guarded(archive)
                    actual = set()
                    for path in archive.iterdir():
                        s.guarded(path)
                        if not path.is_file():
                            errors.append('Invalid archive entry: ' + str(path))
                        else:
                            actual.add(path.name)
                    for missing in sorted(listed - actual):
                        errors.append('Missing archive: ' + missing)
                    for unreferenced in sorted(actual - listed):
                        errors.append('Unreferenced archive: ' + unreferenced)
            class Compare:
                def write(self, path, data):
                    if not path.exists() or path.read_text() != data:
                        errors.append(str(path) + ' stale or missing; run init to rebuild')
            if len(projects) or not any('Project metadata invalid' in e for e in errors):
                s.indexes(Compare())
            if errors:
                raise ValueError('\n'.join(errors))
            return {'ok': True, 'projects': len(projects), 'codebuddy_installed': shutil.which('codebuddy') is not None,
                    'agent_behavior_verified': False}
        if a.command == 'recover':
            if not a.rollback:
                raise ValueError('Inspect .pm-runtime/pending.json; then pass --rollback')
            pending = s.journal.exists()
            rollback(s)
            return {'rolled_back': pending}


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', default=str(Path(__file__).resolve().parent.parent))
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('init', help='Initialize/rebuild indexes; preserve existing projects')
    q = sub.add_parser('index'); q.add_argument('--history', action='store_true')
    q = sub.add_parser('list'); q.add_argument('--all', action='store_true')
    q = sub.add_parser('create')
    for k in ('id', 'name', 'summary'):
        q.add_argument('--' + k, required=True)
    q.add_argument('--type', required=True, choices=TYPES)
    q.add_argument('--confirmed', action='store_true')
    q = sub.add_parser('resume'); q.add_argument('id')
    q = sub.add_parser('work-items'); q.add_argument('id')
    for command in ('checkpoint', 'edit', 'status', 'compact', 'promote', 'describe'):
        q = sub.add_parser(command)
        q.add_argument('id'); q.add_argument('--expected', required=True)
        if command == 'checkpoint':
            q.add_argument('--payload', required=True)
        if command == 'describe':
            q.add_argument('--name'); q.add_argument('--summary'); q.add_argument('--reason', required=True)
        if command == 'edit':
            q.add_argument('--document', choices=('definition.md', 'acceptance.md', 'state.md', 'notes.md', 'source/INDEX.md'), required=True)
            q.add_argument('--file', required=True); q.add_argument('--reason', required=True)
        if command == 'status':
            q.add_argument('--status', choices=STATES, required=True)
            q.add_argument('--reason', required=True); q.add_argument('--confirmed', action='store_true')
        if command == 'compact':
            q.add_argument('--summary-file', required=True)
        if command == 'promote':
            q.add_argument('--title', required=True); q.add_argument('--file', required=True)
            q.add_argument('--reason', required=True); q.add_argument('--confirmed', action='store_true')
    sub.add_parser('doctor')
    q = sub.add_parser('recover'); q.add_argument('--rollback', action='store_true')
    return p


def main():
    try:
        result = run(parser().parse_args())
        print(result if isinstance(result, str) else dump(result), end='\n')
        return 0
    except (ValueError, KeyError, TypeError, OSError) as e:
        print('ERROR: ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
