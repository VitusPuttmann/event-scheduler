"""
Node for loading events.
"""

import os
from datetime import datetime
from typing import Optional

from langchain_core.runnables import RunnableConfig

from scheduler_app.models.event import Event
from scheduler_app.graph.state import AgentState
from scheduler_app.infra.database import load_events_from_db


def load_events(
    state: AgentState, config: Optional[RunnableConfig] = None
) -> dict:
    rows = load_events_from_db(os.environ["DUCKDB_PATH"], state.user_input_date)

    events = []
    for (
        event_id,
        event_name,
        event_date,
        event_time,
        event_venue,
        event_type,
        event_description,
        event_url) in rows:
        t = datetime.strptime(event_time[:5], "%H:%M").time()
        events.append(Event(
            event_id=event_id,
            event_name=event_name,
            event_date=event_date,
            event_time=t,
            event_venue=event_venue,
            event_type=event_type,
            event_description=event_description,
            event_url=event_url
        ))
    
    # Update state
    updated_state = {
        "events_list": events
    }
    return updated_state
