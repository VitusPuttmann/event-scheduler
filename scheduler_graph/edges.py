"""
Conditional edges for the LangGraph application.
"""

import os
from pathlib import Path
from typing import Optional, Literal

import duckdb

from langchain_core.runnables import RunnableConfig

from scheduler_graph.state import AgentState
from scheduler_graph.database import load_events_from_db


EVENTS_TABLE = "events"


def check_data_availability(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> Literal["data_available", "data_not_available"]:
    """
    Check 1) existence of the database, 2) existence of the events table, and
    3) availability of data for the selected day.
    """

    db_exists = Path(os.environ["DUCKDB_PATH"]).exists()
    if not db_exists:
        return "data_not_available"

    with duckdb.connect(os.environ["DUCKDB_PATH"]) as con:
        table_exists = con.execute(
            """
            SELECT 1
              FROM information_schema.tables
             WHERE table_name = ?
            """,
            (EVENTS_TABLE,),
        ).fetchone()

        if not table_exists:
            return "data_not_available"
        
        data_exists = load_events_from_db(
            os.environ["DUCKDB_PATH"], state.user_input_date
        )
        if len(data_exists) == 0:
            return "data_not_available"
        else:
            return "data_available"
