"""
Define nodes for the LangGraph application.
"""

import json
from datetime import datetime
import os
from typing import List, Optional

from langchain_core.runnables import RunnableConfig

from scheduler_graph.state import AgentState
from scheduler_graph.search import WebSearchClient
from scheduler_graph.llm import LLMClient
from models.event import Event


def find_events(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, str]:
    """
    Obtain data with events from web search.
    """

    # Instantiate client
    search_client = WebSearchClient(service=os.environ["WEBSEARCH_SERVICE"])

    # Perform search
    input_date = datetime.strptime(state.user_input_date, "%Y-%m-%d").date()
    response = search_client.client.search(
        f"Veranstaltungen in Hamburg am {input_date}"
    )

    # Update state
    updated_state = {"events_raw": response}
    return updated_state


def format_events(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, List[Event]]:
    """
    Transform raw web search output into JSON and then into list of events.
    """

    # Query LLM to transform unstructured output into JSON
    llm_client = LLMClient(service=os.environ["LLM_SERVICE"])
    
    system_message = """
        Return JSON only. No markdown fences. Use German.
        """
    query_message = """
        Given the input provided as context, identify events in the input,
        including their:
        . type (e.g., "Konzert", "Ausstellung")
        . name (e.g., "Legacy Tour")
        . artists (e.g., "Markus Müller")
        . date (in the format YYYY-MM-DD)
        . start time (in the format HH:MM)
        . end time (in the format HH:MM)
        . venue (e.g., "Elbphilharmonie")
        . description of the event (as plain text in German)
        Return a JSON object with one key that follows the structure:
            {
              "events": [
                {
                  "type": "…",
                  "name": "…",
                  "artists": "…",
                  "date": "2026-02-02",
                  "start": "19:30",
                  "end": "22:00",
                  "venue": "…",
                  "description": "…"
                }
              ]
            }
        """
    context=json.dumps(state.events_raw, ensure_ascii=False)

    llm_output = llm_client.query(system_message, query_message, context)

    try:
        payload = json.loads(llm_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM did not return valid JSON: {e}") from e

    # Store entries as list of events to be stored in state
    events = []
    for entry in payload.get("events", []):
        event = Event.from_dict(entry)
        events.append(event)

    # Update state
    updated_state = {"events_list": events}
    return updated_state


def filter_events(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, List[Event]]:
    """
    Filter list of events based on initial user input on preferred event type.
    """

    # Obtain initial list of events
    events_initial = state.events_list

    # Obtain user input on desired date as date
    input_type = state.user_input_type.lower().strip()

    # Filter event list based on user input
    events_filtered = [
        e for e in events_initial if e.event_type.lower().strip() == input_type
    ]

    # Update state
    updated_state = {"events_list": events_filtered}
    return updated_state


def finalize_output(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, str]:

    # Query LLM for final output message
    llm_client = LLMClient(service=os.environ["LLM_SERVICE"])
    
    system_message = """
        You are a friendly guide that provides helpful event suggestions in German.
        """
    query_message = """
        Given the input provided as context, produce a text that presents the
        events in the list with as much information as possible.
        If there are no events in the list, only state kindly that there are no
        suitable events (without offering any further assistance).
        """
    context=state.events_list

    events_text = llm_client.query(system_message, query_message, context)

    # Update state
    updated_state = {"output": events_text}
    return updated_state
