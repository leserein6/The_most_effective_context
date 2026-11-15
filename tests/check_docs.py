#!/usr/bin/env python3
"""检查 Markdown 本地相对链接是否存在。仅用 Python 标准库。"""
from pathlib import Path
from urllib.parse import unquote
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SKIP_PREFIX = ("https://", "http://", "mailto:", "sandbox:", "#")

def main() -> int:
    issues = []
    scanned = 0
    for file in sorted(ROOT.rglob("*.md")):
        if ".git" in file.parts:
            continue
        scanned += 1
        for line_no, line in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
            for match in LINK.finditer(line):
                raw = match.group(1).split(" ", 1)[0]
                if raw.startswith(SKIP_PREFIX):
                    continue
                target = unquote(raw.split("#", 1)[0]).split("?", 1)[0]
                if target and not (file.parent / target).exists():
                    issues.append(f"{file.relative_to(ROOT)}:{line_no}: missing {raw}")
    for item in issues:
        print(item)
    print(f"Checked {scanned} Markdown files; broken local links: {len(issues)}")
    return 1 if issues else 0

if __name__ == "__main__":
    sys.exit(main())
