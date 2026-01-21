"""
Unit tests for database connection.
"""

from datetime import date, time
import pytest

import duckdb

from models.event import Event
from scheduler_graph.database import (
    ensure_table,
    persist_events_to_db,
    load_events_from_db,
    EVENTS_TABLE
)


def test_ensure_table_creates_when_missing(tmp_path):
    db_path = tmp_path / "test.duckdb"

    with duckdb.connect(str(db_path)) as con:
        ensure_table(con, "events")

        exists = con.execute(
            """
            SELECT 1
              FROM information_schema.tables
             WHERE table_name = ?""",
             ("events",),
        ).fetchone()

        assert exists is not None


def test_ensure_table_is_idempotent(tmp_path):
    db_path = tmp_path / "test.duckdb"

    with duckdb.connect(str(db_path)) as con:
        ensure_table(con, "events")
        ensure_table(con, "events")

        exists = con.execute(
            """
            SELECT 1
              FROM information_schema.tables
             WHERE table_name = ?""",
            ("events",),
        ).fetchone()

        assert exists is not None


def _get_event_row(con: duckdb.DuckDBPyConnection, event_id: str):
    return con.execute(
        f"""
        SELECT event_id, event_name, event_date, event_time,
               event_venue, event_type, event_description, event_url
          FROM {EVENTS_TABLE}
         WHERE event_id = ?
        """,
        (event_id,),
    ).fetchone()


def test_persist_events_inserts_new_rows(tmp_path):
    db_path = str(tmp_path / "test.duckdb")

    e = Event(
        event_id="testid",
        event_name="Test Name",
        event_date=date(2020, 1, 2),
        event_time=time(20, 0),
        event_venue="Test Venue",
        event_type="Test Type",
        event_description="A test description.",
        event_url="https://test.org/test",
    )

    persist_events_to_db(db_path, [e])

    with duckdb.connect(db_path) as con:
        ensure_table(con, EVENTS_TABLE)
        assert _get_event_row(con, "testid") == (
            "testid",
            "Test Name",
            date(2020, 1, 2),
            "20:00:00",
            "Test Venue",
            "Test Type",
            "A test description.",
            "https://test.org/test",
        )


def test_persist_events_upsert_keeps_existing_when_new_is_none(tmp_path):
    db_path = str(tmp_path / "test.duckdb")

    e1 = Event(
        event_id="testid",
        event_name="Test Name",
        event_date=date(2020, 1, 2),
        event_time=time(20, 0),
        event_venue="Test Venue",
        event_type="Test Type",
        event_description="A test description.",
        event_url="https://test.org/test",
    )
    persist_events_to_db(db_path, [e1])

    e2 = Event(
        event_id="testid",
        event_name="Test Name",
        event_date=date(2020, 1, 2),
        event_time=time(20, 0),
        event_venue="Test Venue",
        event_type=None,
        event_description=None,
        event_url=None,
    )
    persist_events_to_db(db_path, [e2])

    with duckdb.connect(db_path) as con:
        ensure_table(con, EVENTS_TABLE)
        row = _get_event_row(con, "testid")
        assert row[5] == "Test Type"
        assert row[6] == "A test description."
        assert row[7] == "https://test.org/test"


def test_persist_events_upsert_updates_when_new_is_not_none(tmp_path):
    db_path = str(tmp_path / "test.duckdb")

    e1 = Event(
        event_id="testid",
        event_name="Test Name",
        event_date=date(2020, 1, 2),
        event_time=time(20, 0),
        event_venue="Test Venue",
        event_type="Type Old",
        event_description="An old description.",
        event_url="https://test.org/old",
    )
    persist_events_to_db(db_path, [e1])

    e2 = Event(
        event_id="testid",
        event_name="Test Name",
        event_date=date(2020, 1, 2),
        event_time=time(20, 0),
        event_venue="Test Venue",
        event_type="Type New",
        event_description="A new description.",
        event_url="https://test.org/new",
    )
    persist_events_to_db(db_path, [e2])

    with duckdb.connect(db_path) as con:
        ensure_table(con, EVENTS_TABLE)
        row = _get_event_row(con, "testid")
        assert row[5] == "Type New"
        assert row[6] == "A new description."
        assert row[7] == "https://test.org/new"


def test_load_events_returns_content(tmp_path):
    db_path = str(tmp_path / "test.duckdb")

    e = Event(
        event_id="testid",
        event_name="Test Name",
        event_date=date(2020, 1, 2),
        event_time=time(20, 0),
        event_venue="Test Venue",
        event_type="Test Type",
        event_description="A test description.",
        event_url="https://test.org/test",
    )

    persist_events_to_db(db_path, [e])
    
    events = load_events_from_db(db_path, "2020-01-02")

    assert events[0][0] == "testid"
    assert events[0][1] == "Test Name"
    assert events[0][2] == date(2020, 1, 2)
    assert events[0][3] == "20:00:00"
    assert events[0][4] == "Test Venue"
    assert events[0][5] == "Test Type"
    assert events[0][6] == "A test description."
    assert events[0][7] == "https://test.org/test"
