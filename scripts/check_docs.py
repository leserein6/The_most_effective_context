#!/usr/bin/env python3
"""Reject accidental literal newline escapes and unclosed Markdown fences."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ('docs', 'entry', 'project-management', 'evidence/methods')
errors = []
for source in SOURCES:
    for path in sorted((ROOT / source).rglob('*.md')):
        if '/projects/' in path.as_posix():
            continue
        fenced = False
        for lineno, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            trimmed = line.lstrip()
            if trimmed.startswith('~~~') or trimmed.startswith(chr(96) * 3):
                fenced = not fenced
                continue
            if fenced:
                continue
            mark = chr(96)
            prose = re.sub(mark + '[^' + mark + ']*' + mark, '', line)
            if r'\n' in prose:
                errors.append('{}:{} literal newline escape outside code'.format(
                    path.relative_to(ROOT), lineno))
        if fenced:
            errors.append('{}: unclosed code fence'.format(path.relative_to(ROOT)))
if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)
print('Maintained Markdown structure OK')
