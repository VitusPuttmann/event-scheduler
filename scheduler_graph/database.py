"""
Database access for loading and persisting events.
"""

from typing import List

import duckdb

from models.event import Event


EVENTS_TABLE = "events"


def ensure_table(con: duckdb.DuckDBPyConnection, table_name: str) -> None:
    exists = con.execute(
            """
            SELECT 1
              FROM information_schema.tables
             WHERE table_name = ?
            """,
            (table_name,),
        ).fetchone()

    if exists is None:
        con.execute(
            f"""
            CREATE TABLE {table_name} (
                event_id TEXT PRIMARY KEY,
                event_name TEXT NOT NULL,
                event_date DATE NOT NULL,
                event_time TEXT NOT NULL,
                event_venue TEXT,
                event_type TEXT,
                event_description TEXT,
                event_url TEXT
            )
            """
        )


def persist_events_to_db(db_path: str, events: List[Event]) -> None:
    with duckdb.connect(db_path) as con:

        ensure_table(con, EVENTS_TABLE)

        con.executemany(
            f"""
            INSERT INTO {EVENTS_TABLE}
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (event_id) DO UPDATE SET
                event_type = COALESCE(EXCLUDED.event_type, {EVENTS_TABLE}.event_type),
                event_description = COALESCE(EXCLUDED.event_description, {EVENTS_TABLE}.event_description),
                event_url = COALESCE(EXCLUDED.event_url, {EVENTS_TABLE}.event_url)
            """,
            [e.to_tuple() for e in events],
        )


def load_events_from_db(db_path: str, select_date: str) -> List[tuple]:
    with duckdb.connect(db_path) as con:
        result = con.execute(
            f"""
            SELECT *
              FROM {EVENTS_TABLE}
             WHERE event_date = ?""",
            [select_date],
        ).fetchall()
    return result
