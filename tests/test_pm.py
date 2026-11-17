import base64
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/pm.py'
spec = importlib.util.spec_from_file_location('pm', SCRIPT)
pm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pm)


class ProjectFlow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.call('init')

    def tearDown(self):
        self.temp.cleanup()

    def cmd(self, *args):
        return [sys.executable, str(SCRIPT), '--root', str(self.root), *args]

    def call(self, *args, ok=True):
        r = subprocess.run(self.cmd(*args), capture_output=True, text=True)
        if ok:
            self.assertEqual(r.returncode, 0, r.stderr)
        else:
            self.assertNotEqual(r.returncode, 0, r.stdout)
        try:
            return json.loads(r.stdout)
        except ValueError:
            return r.stdout if ok else r.stderr

    def create(self, pid='demo', typ='development'):
        return self.call('create', '--id', pid, '--name', '示例项目', '--summary', '可验证的独立目标', '--type', typ, '--confirmed')

    def token(self, pid='demo'):
        return self.call('resume', pid)['token']

    def payload(self, turn='turn-1', phase=False):
        p = self.root / (turn + '.json')
        p.write_text(json.dumps({'turn_id': turn, 'mode': 'execute', 'progress': '实现加法并验证',
            'next': '边界审查', 'open_questions': ['是否处理溢出'], 'operations': ['读取需求', '实现函数', '运行验证'],
            'evidence': [{'kind': 'observed', 'claim': '两项验证通过', 'source': '本轮命令输出'}],
            'outcome': '通过已定义检查，尚未声明项目完成', 'phase_end': phase,
            'decisions': [{'text': '使用标准库', 'status': 'confirmed', 'user_evidence': '用户明确同意'}]}), encoding='utf-8')
        return str(p)

    def test_full_lifecycle_and_cross_session(self):
        self.create()
        data = self.call('checkpoint', 'demo', '--expected', self.token(), '--payload', self.payload())
        resumed = self.call('resume', 'demo')
        self.assertIn('实现加法', resumed['files']['state.md'])
        self.assertIn('使用标准库', resumed['files']['decisions.md'])
        archive = self.call('status', 'demo', '--expected', data['token'], '--status', 'archived', '--reason', '用户暂缓', '--confirmed')
        self.assertIn('/archived/', archive['path'])
        self.assertNotIn('示例项目', self.call('index'))
        self.assertIn('示例项目', self.call('index', '--history'))
        self.call('status', 'demo', '--expected', archive['token'], '--status', 'active', '--reason', '用户恢复', '--confirmed')
        self.call('status', 'demo', '--expected', self.token(), '--status', 'completed', '--reason', '用户确认达成目标', '--confirmed')
        self.assertTrue(self.call('doctor')['ok'])

    def test_three_types_and_unique_identity(self):
        for i, typ in enumerate(pm.TYPES):
            self.create('demo-' + str(i), typ)
        self.assertEqual(len(self.call('list')), 3)
        self.call('create', '--id', 'demo-0', '--name', '重复', '--summary', '重复', '--type', 'learning', '--confirmed', ok=False)

    def test_status_preserves_executable_permissions(self):
        p = Path(self.create()['path'])
        f = p / 'work/run.sh'; f.write_text('#!/bin/sh\nexit 0\n'); f.chmod(0o755)
        result = self.call('status', 'demo', '--expected', self.token(), '--status', 'archived', '--reason', '用户暂停', '--confirmed')
        self.assertEqual((Path(result['path']) / 'work/run.sh').stat().st_mode & 0o777, 0o755)

    def test_recovery_rejects_path_escape(self):
        victim = self.root.parent / (self.root.name + '-victim')
        victim.write_text('必须保留')
        try:
            pending = self.root / '.pm-runtime/pending.json'
            pending.write_text(json.dumps({'before': {'project-management/../../' + victim.name: None}}))
            self.call('recover', '--rollback', ok=False)
            self.assertEqual(victim.read_text(), '必须保留')
        finally:
            victim.unlink()

    def test_no_unconfirmed_create_or_status(self):
        self.call('create', '--id', 'demo', '--name', '测试', '--summary', '目标', '--type', 'one_off', ok=False)
        self.assertEqual(self.call('list'), [])
        self.create()
        self.call('status', 'demo', '--expected', self.token(), '--status', 'completed', '--reason', '猜测', ok=False)
        self.assertEqual(self.call('list')[0]['status'], 'active')

    def test_stale_state_and_direct_file_edit_conflict(self):
        p = Path(self.create()['path'])
        token = self.token()
        (p / 'notes.md').write_text('另一个会话的新知识', encoding='utf-8')
        error = self.call('checkpoint', 'demo', '--expected', token, '--payload', self.payload(), ok=False)
        self.assertIn('CONFLICT', error)
        self.assertEqual((p / 'notes.md').read_text(), '另一个会话的新知识')

    def test_work_outputs_do_not_invalidate_shared_state_token(self):
        p = Path(self.create()['path']); token = self.token()
        (p / 'work/main.py').write_text('print(1 + 1)')
        self.call('checkpoint', 'demo', '--expected', token, '--payload', self.payload())

    def test_summary_update_refreshes_index(self):
        self.create()
        self.call('describe', 'demo', '--expected', self.token(), '--summary', '用户修改后的独立目标', '--reason', '用户明确修订')
        self.assertIn('用户修改后的独立目标', self.call('index'))

    def test_long_term_definition_survives_progress_updates(self):
        self.create()
        definition = self.root / 'definition.md'
        definition.write_text('# 项目定义\n\n问题：跨会话丢进度\n范围：仅本地\n约束：不得自动提交 Git\n')
        self.call('edit', 'demo', '--expected', self.token(), '--document', 'definition.md', '--file', str(definition), '--reason', '用户明确约束')
        self.call('checkpoint', 'demo', '--expected', self.token(), '--payload', self.payload())
        state = self.call('resume', 'demo')
        self.assertIn('不得自动提交 Git', state['files']['definition.md'])
        self.assertIn('仅本地', state['files']['definition.md'])

    def test_concurrent_updates_only_one_commits(self):
        self.create()
        token = self.token()
        processes = [subprocess.Popen(self.cmd('checkpoint', 'demo', '--expected', token,
                     '--payload', self.payload('turn-' + str(i))), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for i in range(2)]
        results = [p.communicate() for p in processes]
        self.assertEqual(sorted(p.returncode for p in processes), [0, 2], results)
        self.assertTrue(any('CONFLICT' in stderr for _, stderr in results))

    def test_compaction_preserves_exact_bytes(self):
        p = Path(self.create()['path'])
        self.call('checkpoint', 'demo', '--expected', self.token(), '--payload', self.payload(phase=True))
        self.assertTrue(self.call('resume', 'demo')['compression_due'])
        original = (p / 'logs/current.md').read_bytes()
        summary = self.root / 'summary.md'
        summary.write_text('## 已完成\n实现加法\n## 决策\n标准库\n## 未解决\n溢出\n## 恢复位置\n边界审查\n')
        result = self.call('compact', 'demo', '--expected', self.token(), '--summary-file', str(summary))
        self.assertEqual((p / result['archive']).read_bytes(), original)
        self.assertFalse(self.call('resume', 'demo')['compression_due'])
        self.assertTrue(self.call('doctor')['ok'])
        (p / result['archive']).write_text('破坏原文')
        self.assertIn('integrity', self.call('doctor', ok=False))

    def test_invalid_payload_has_no_partial_writes(self):
        p = Path(self.create()['path'])
        token = self.token()
        payload = Path(self.payload())
        data = json.loads(payload.read_text())
        data['decisions'][0].pop('user_evidence')
        payload.write_text(json.dumps(data))
        self.call('checkpoint', 'demo', '--expected', token, '--payload', str(payload), ok=False)
        self.assertEqual(token, self.token())
        self.assertFalse((self.root / '.pm-runtime/pending.json').exists())

    def test_duplicate_turn_rejected_after_refresh(self):
        self.create()
        payload = self.payload()
        self.call('checkpoint', 'demo', '--expected', self.token(), '--payload', payload)
        self.assertIn('Duplicate', self.call('checkpoint', 'demo', '--expected', self.token(), '--payload', payload, ok=False))

    def test_crash_requires_explicit_recovery(self):
        p = Path(self.create()['path'])
        original = (p / 'state.md').read_bytes()
        code = '''import importlib.util,os,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('pm',sys.argv[1]);pm=importlib.util.module_from_spec(spec);spec.loader.exec_module(pm)
s=pm.Store(sys.argv[2])
with s.lock():
    tx=pm.Transaction(s)
    tx.write(Path(sys.argv[3]),'模拟中断后的新状态')
    os._exit(9)
'''
        subprocess.run([sys.executable, '-c', code, str(SCRIPT), str(self.root), str(p / 'state.md')], check=False)
        self.assertIn('Interrupted', self.call('resume', 'demo', ok=False))
        self.call('recover', '--rollback')
        self.assertEqual((p / 'state.md').read_bytes(), original)
        self.assertTrue(self.call('doctor')['ok'])

    def test_symlink_and_traversal_rejected(self):
        self.call('create', '--id', '../evil', '--name', '恶意', '--summary', '恶意', '--type', 'one_off', '--confirmed', ok=False)
        p = Path(self.create()['path'])
        outside = self.root / 'external'
        outside.mkdir()
        (p / 'work/external').symlink_to(outside, target_is_directory=True)
        self.assertIn('Symlink', self.call('resume', 'demo', ok=False))

    def test_public_promotion_requires_confirmation(self):
        self.create()
        f = self.root / 'candidate.md'; f.write_text('跨项目可复用的结论')
        args = ('promote', 'demo', '--expected', self.token(), '--title', '经验', '--file', str(f), '--reason', '用户确认')
        self.call(*args, ok=False)
        self.call(*args, '--confirmed')
        self.assertIn('跨项目', (self.root / 'project-management/conventions/README.md').read_text())

    def test_document_edit_and_index_regeneration(self):
        self.create()
        f = self.root / 'acceptance.md'; f.write_text('# 验收条件\n\n能恢复项目；并发覆盖被拒绝。')
        self.call('edit', 'demo', '--expected', self.token(), '--document', 'acceptance.md', '--file', str(f), '--reason', '明确验收')
        self.assertIn('并发覆盖', self.call('resume', 'demo')['files']['acceptance.md'])
        (self.root / 'project-management/Index.md').write_text('过期索引')
        self.call('doctor', ok=False)
        self.call('init')
        self.assertTrue(self.call('doctor')['ok'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
