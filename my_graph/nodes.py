"""
Define nodes for the LangGraph application.
"""

from datetime import datetime
from typing import List, Optional

from langchain_core.runnables import RunnableConfig

from my_graph.state import AgentState
from models.event import Event


def find_events(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, List[Event]]:
    """
    Obtain initial list of potentially relevant events.
    """

    import csv

    # Import csv with raw data
    with open("data/raw/events.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        entries = list(reader)
    
    # Store entries as list of events to be stored in state
    events = []
    for entry in entries:
        event = Event.from_dict(entry)
        events.append(event)
    
    # Update state
    updated_state = {"events": events}
    return updated_state


def filter_events(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, List[Event]]:
    """
    Filter list of events based on initial user input.
    """

    # Obtain initial list of events
    events_initial = state.events

    # Obtain user input on desired date as date
    input_date = datetime.strptime(state.user_input, "%Y-%m-%d").date()

    # Filter event list based on user input
    events_filtered = [e for e in events_initial if e.event_date == input_date]

    # Update state
    updated_state = {"events": events_filtered}
    return updated_state


def finalize_output(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, str]:

    # Obtain final list of events
    events_final = state.events

    # Transform list into output text
    if events_final:
        events_text = (
            "\nEine relevante Veranstaltung für Dich ist:\n"
            f"{events_final[0].event_name} mit {events_final[0].event_artists}\n"
            f"am {events_final[0].event_date} um {events_final[0].event_start_time}\n"
            f"in der {events_final[0].event_venue}\n"
        )
    else:
        events_text = "Es gibt leider keine relevante Veranstaltung für Dich."

    # Update state
    updated_state = {"output": events_text}
    return updated_state
