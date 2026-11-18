"""Import a headerless UTF-8 CSV into a local SQLite book list."""
import csv
from contextlib import closing
from pathlib import Path
import sqlite3
import sys


def import_books(db, csv_file):
    with closing(sqlite3.connect(db)) as conn, conn:
        conn.execute("CREATE TABLE IF NOT EXISTS books (id TEXT PRIMARY KEY, title TEXT NOT NULL)")
        with Path(csv_file).open(encoding="utf-8", newline="") as stream:
            for book, title in csv.reader(stream):
                if not title.strip():
                    raise ValueError("empty title")
                conn.execute("INSERT INTO books VALUES (?, ?)", (book, title))


if __name__ == "__main__":
    try:
        import_books(*sys.argv[1:])
    except (ValueError, sqlite3.Error, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
