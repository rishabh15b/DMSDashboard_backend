"""
Migration script to add msa_number column to the documents table.

Usage:
    python scripts/migrate_add_msa_number.py
"""

import os
import sqlite3
from pathlib import Path


DB_PATH = Path(os.getenv("DATABASE_PATH", "dms_database.db"))


def column_exists(cursor, column_name: str) -> bool:
    cursor.execute("PRAGMA table_info(documents)")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns


def add_msa_column():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        migrations = []

        if not column_exists(cursor, "msa_number"):
            print("➕ Adding msa_number column to documents table...")
            cursor.execute("ALTER TABLE documents ADD COLUMN msa_number TEXT")
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS ix_documents_msa_number ON documents(msa_number)"
            )
            migrations.append("msa_number")
        else:
            print("✓ msa_number column already exists")

        conn.commit()

        if migrations:
            print("Migration complete:", ", ".join(migrations))
        else:
            print("No changes applied.")
    finally:
        conn.close()


if __name__ == "__main__":
    add_msa_column()

