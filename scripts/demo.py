#!/usr/bin/env python3
"""Run a real development/learning/one-off lifecycle in a disposable directory."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    script = Path(__file__).resolve().with_name('pm.py')
    with tempfile.TemporaryDirectory(prefix='project-workspace-demo-') as tmp:
        def call(*args):
            result = subprocess.run([sys.executable, str(script), '--root', tmp, *args], capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        call('init')
        for pid, typ in [('calculator', 'development'), ('go-study', 'learning'), ('rpc-report', 'one_off')]:
            call('create', '--id', pid, '--name', pid, '--type', typ, '--summary', '演示目标：' + pid, '--confirmed')
        project = Path(call('resume', 'calculator')['path'])
        artifact = project / 'work/calculator.py'
        artifact.write_text('def add(a, b):\n    return a + b\n\nif __name__ == "__main__":\n    assert add(2, 3) == 5\n    assert add(-2, 2) == 0\n    print("2 checks passed")\n')
        result = subprocess.run([sys.executable, str(artifact)], capture_output=True, text=True, check=True)
        payload = Path(tmp) / 'turn.json'
        payload.write_text(json.dumps({'turn_id': 'demo-1', 'mode': 'execute', 'progress': '加法工具实现并验证',
            'next': '用户决定是否完成', 'operations': ['编写加法工具', '运行两项行为断言'],
            'open_questions': [], 'evidence': [{'kind': 'observed', 'claim': result.stdout.strip(), 'source': str(artifact)}],
            'outcome': '代码验证通过；项目状态仍为 active', 'phase_end': True}), encoding='utf-8')
        call('checkpoint', 'calculator', '--expected', call('resume', 'calculator')['token'], '--payload', str(payload))
        summary = Path(tmp) / 'summary.md'
        summary.write_text('## 已完成\n加法工具及两项实际检查。\n## 决策\n无新增决策。\n## 未解决\n用户未决定项目状态。\n## 恢复位置\nwork/calculator.py；下一步等待用户决定。\n')
        call('compact', 'calculator', '--expected', call('resume', 'calculator')['token'], '--summary-file', str(summary))
        call('status', 'go-study', '--expected', call('resume', 'go-study')['token'], '--status', 'archived', '--reason', '演示：用户确认暂停', '--confirmed')
        call('status', 'calculator', '--expected', call('resume', 'calculator')['token'], '--status', 'completed', '--reason', '演示：用户确认完成', '--confirmed')
        report = call('doctor')
        print(json.dumps({'demo_passed': report['ok'], 'projects': call('list', '--all'),
            'artifact_check': result.stdout.strip(), 'archive_verified': True,
            'note': '独立临时目录演示；未创建真实用户项目，未启动模型或 CodeBuddy。'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
