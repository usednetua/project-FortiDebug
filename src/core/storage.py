"""SQLite storage for saved commands."""

import sqlite3
import os
from datetime import datetime
from pathlib import Path


def _db_path() -> Path:
    appdata = os.environ.get("APPDATA") or str(Path.home())
    folder = Path(appdata) / "FortiDebugBuilder"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "commands.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            command TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def save_command(title: str, command: str, category: str = "", notes: str = "") -> int:
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO commands (title, category, notes, command, created_at) VALUES (?, ?, ?, ?, ?)",
        (title, category, notes, command, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def list_commands(search: str = "") -> list:
    conn = get_connection()
    if search.strip():
        q = f"%{search.strip()}%"
        rows = conn.execute(
            """
            SELECT * FROM commands
            WHERE title LIKE ? OR category LIKE ? OR notes LIKE ? OR command LIKE ?
            ORDER BY created_at DESC
            """,
            (q, q, q, q),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM commands ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_command(cmd_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM commands WHERE id = ?", (cmd_id,))
    conn.commit()
    conn.close()


def update_command(cmd_id: int, title: str, category: str, notes: str) -> None:
    conn = get_connection()
    conn.execute(
        "UPDATE commands SET title = ?, category = ?, notes = ? WHERE id = ?",
        (title, category, notes, cmd_id),
    )
    conn.commit()
    conn.close()
