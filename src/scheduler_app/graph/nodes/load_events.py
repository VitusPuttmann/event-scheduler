"""
Node for loading events.
"""

import os
from typing import Optional

from langchain_core.runnables import RunnableConfig

from scheduler_app.models.event import Event
from scheduler_app.graph.state import AgentState
from scheduler_app.infra.database import load_events_from_db


def load_events(
    state: AgentState, config: Optional[RunnableConfig] = None
) -> dict:
    rows = load_events_from_db(os.environ["DUCKDB_PATH"], state.user_input_date)

    events = [
        Event.from_dict({
            "event_id":          row[0],
            "event_name":        row[1],
            "event_date":        row[2].isoformat(),
            "event_time":        row[3][:5],
            "event_venue":       row[4],
            "event_type":        row[5],
            "event_description": row[6],
            "event_url":         row[7],
        })
        for row in rows
    ]
    
    # Update state
    updated_state = {
        "events_list": events
    }
    return updated_state
