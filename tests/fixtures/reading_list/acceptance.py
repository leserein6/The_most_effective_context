"""Independent CLI acceptance checks. Emit JUnit using only the standard library."""
from contextlib import closing
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
import xml.etree.ElementTree as ET


class ReadingList(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.db = Path(directory.name) / "books.db"
        self.csv = self.db.with_suffix(".csv")
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.execute("CREATE TABLE books (id TEXT PRIMARY KEY, title TEXT NOT NULL)")
            conn.execute("INSERT INTO books VALUES ('A', 'Atlas')")

    def run_import(self, text):
        self.csv.write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, str(Path(__file__).with_name("books.py")),
                               str(self.db), str(self.csv)], capture_output=True, text=True)

    def reopened(self):
        with closing(sqlite3.connect(self.db)) as reader:
            return reader.execute("SELECT id, title FROM books ORDER BY id").fetchall()

    def test_valid_batch(self):
        result = self.run_import("B,Birds\nC,Clouds\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.reopened(), [("A", "Atlas"), ("B", "Birds"), ("C", "Clouds")])

    def test_rejected_batch(self):
        result = self.run_import("B,Birds\nC,\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty title", result.stderr)
        self.assertEqual(self.reopened(), [("A", "Atlas")])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReadingList)
    tests = list(suite)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    xml = ET.Element("testsuite", name="books")
    elements = {test: ET.SubElement(xml, "testcase", classname="ReadingList",
                                    name=test._testMethodName) for test in tests}
    for tag, outcomes in (("failure", result.failures), ("error", result.errors), ("skipped", result.skipped)):
        for test, detail in outcomes:
            ET.SubElement(elements[test], tag).text = detail
    ET.ElementTree(xml).write(os.environ["HARNESS_JUNIT"], encoding="utf-8")
    sys.exit(0 if result.wasSuccessful() else 1)
