from __future__ import annotations

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "library.sqlite"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"
SEED_PATH = PROJECT_ROOT / "sql" / "seed.sql"


def connect(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """SQLite veritabanina baglanti acar ve foreign key kontrolunu etkinlestirir."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def run_script(connection: sqlite3.Connection, script_path: Path) -> None:
    script = script_path.read_text(encoding="utf-8")
    connection.executescript(script)
    connection.commit()


def initialize_database(
    db_path: str | Path = DEFAULT_DB_PATH,
    with_seed: bool = True,
) -> sqlite3.Connection:
    connection = connect(db_path)
    run_script(connection, SCHEMA_PATH)

    if with_seed:
        run_script(connection, SEED_PATH)

    return connection
