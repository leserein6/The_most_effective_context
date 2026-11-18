import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts/test_gate.py"
BOOKS = ROOT / "tests/fixtures/reading_list"


class TestingFlow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.plan = self.work / "plan.json"
        self.plan.write_text(json.dumps({"schema": "testing/v1", "criteria": [
            {"id": "R", "source": "contract", "expected": "visible effect", "cases": ["C::effect"]}]}))

    def run_gate(self, *cmd, out="run"):
        return subprocess.run([sys.executable, str(GATE), "--candidate", "fixture",
                               "--plan", str(self.plan), "--out", out, "--", *cmd],
                              cwd=self.work, capture_output=True, text=True)

    def test_cli_book_contract(self):
        shutil.copytree(BOOKS, self.work / "book")
        self.plan.write_bytes((BOOKS / "plan.json").read_bytes())
        cmd = (sys.executable, "book/acceptance.py")
        self.assertEqual(self.run_gate(*cmd, out="good").returncode, 0)
        product = self.work / "book/books.py"
        original = product.read_text()
        marker = 'conn.execute("INSERT INTO books VALUES (?, ?)", (book, title))'
        self.assertIn(marker, original)
        product.write_text(original.replace(marker, marker + "\n                conn.commit()"))
        self.assertEqual(self.run_gate(*cmd, out="bad").returncode, 1)
        rows = json.loads((self.work / "bad/result.json").read_text())["criteria"]
        self.assertEqual([row["status"] for row in rows], ["PASS", "FAIL"])
        # A valid implementation can stage every row before writing.
        product.write_text(original.replace("for book, title in csv.reader(stream):",
            "rows = list(csv.reader(stream))\n            for book, title in rows:").replace(
            marker, "conn.executemany(\"INSERT INTO books VALUES (?, ?)\", rows)").replace(
            "                conn.executemany", "            conn.executemany"))
        self.assertEqual(self.run_gate(*cmd, out="alternative").returncode, 0)

    def test_missing_output_command_or_malformed_report_blocks(self):
        for i, cmd in enumerate((["no-such-harness-test-command"], [sys.executable, "-c", "pass"],
                [sys.executable, "-c", "import pathlib,sys; pathlib.Path(sys.argv[1]).write_text('<')", "{junit}"])):
            self.assertEqual(self.run_gate(*cmd, out=str(i)).returncode, 2)
            self.assertEqual(json.loads((self.work / str(i) / "result.json").read_text())["status"], "UNVERIFIED")

    def test_case_mapping_and_exit_status(self):
        for index, (names, code, expected) in enumerate((
            ([("effect", None)], 0, 0), ([("effect", "skipped")], 0, 2),
            ([("effect", "error")], 0, 2), ([("other", None)], 0, 2),
            ([("effect", None), ("effect", None)], 0, 2), ([("effect", None)], 3, 2),
            ([("effect", None), ("other", "failure")], 1, 1),
        )):
            root = ET.Element("testsuite")
            for name, child in names:
                case = ET.SubElement(root, "testcase", classname="C", name=name)
                if child:
                    ET.SubElement(case, child)
            (self.work / "input.xml").write_bytes(ET.tostring(root))
            cmd = [sys.executable, "-c", "import shutil,sys; shutil.copyfile('input.xml',sys.argv[1]); sys.exit(int(sys.argv[2]))",
                   "{junit}", str(code)]
            self.assertEqual(self.run_gate(*cmd, out=str(index)).returncode, expected)
        target = self.work / "0/result.json"
        meta = json.loads(target.read_text())
        self.assertEqual(meta["design_adequacy"], "UNVERIFIED")
        self.assertIn("declared criteria", meta["evidence_scope"])
        self.assertIn("caller_supplied", meta["candidate_binding"])
        old = target.read_bytes()
        self.assertEqual(self.run_gate(sys.executable, "-V", out="0").returncode, 2)
        self.assertEqual(target.read_bytes(), old)

    def test_invalid_plan_cannot_pass(self):
        for value in ({}, {"schema": "testing/v1", "criteria": []}):
            self.plan.write_text(json.dumps(value))
            self.assertEqual(self.run_gate(sys.executable, "-V").returncode, 2)
            self.assertFalse((self.work / "run").exists())
