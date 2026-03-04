"""
Node for findings events.
"""

import os
from typing import List, Optional

from langchain_core.runnables import RunnableConfig

from scheduler_app.models.event import Event
from scheduler_app.graph.state import AgentState
from scheduler_app.infra.crawler import fetch_website
from scheduler_app.services.parser import extract_events
from scheduler_app.infra.database import persist_events_to_db


def find_events(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, List[Event]]:
    """
    Obtain and prepare data with events from web scraping.
    """

    # Crawl web page
    date, url, html = fetch_website(state.user_input_date)
    
    # Parse output
    events = extract_events(html, url)

    # Persist events to database
    persist_events_to_db(os.environ["DUCKDB_PATH"], events)
    
    # Update state
    updated_state = {"events_raw": events}
    return updated_state
