"""
Nodes for the LangGraph application.
"""

from __future__ import annotations

import os
import json
from pydantic import ValidationError
from typing import List, Optional

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage

from models.event import Event, AugmentationResult, dicts_to_events
from scheduler_graph.state import AgentState
from scheduler_graph.crawler import fetch_website
from scheduler_graph.parser import extract_events
from scheduler_graph.database import persist_events_to_db, load_events_from_db
from scheduler_graph.llm import create_llm_client


MAX_RETRIES = 3


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


def augment_events(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, List[Event]]:
    """
    Augment data via LLM.
    """

    # Load events from database
    events_list_tuples = load_events_from_db(
        os.environ["DUCKDB_PATH"], state.user_input_date
    )

    # Prepare events for LLM ingestion
    events_list_dicts = []
    for (
        event_id,
        event_name,
        event_date,
        event_time,
        event_venue,
        event_type,
        event_description,
        event_url,
    ) in events_list_tuples:
        events_list_dicts.append(
            {
                "event_id": event_id,
                "event_name": event_name,
                "event_date": event_date.isoformat(),
                "event_time": event_time[:5],
                "event_venue": event_venue,
                "event_url": event_url,
                "event_type": event_type,
                "event_description": event_description,
            }
        )

    # Query LLM to define event type and expand event description
    llm_client = create_llm_client(service=os.environ["LLM_SERVICE"])

    augmenter = llm_client.with_structured_output(AugmentationResult)

    system_message = """
        You augment information on events. Only fill event_type and
        event_description.
        Infer event_type from the event_name and event_description. Do not
        invent facts.
        """
    query_message = """
        Return patches.
        """
    context=json.dumps(events_list_dicts, ensure_ascii=False)

    msg = [
        ("system", system_message),
        ("user", query_message),
        ("user", context),
    ]

    patches = []
    for attempt in range(MAX_RETRIES):
        try:
            llm_output: AugmentationResult = augmenter.invoke(msg)
            patches = llm_output.patches
            break
        except ValidationError:
            if attempt == MAX_RETRIES - 1:
                patches = []

    for patch in patches:
        patch_clean = {
            k: v for k, v in patch.model_dump().items()
            if v is not None and k != "event_id"}
        
        idx = next(
            (i for i, d in enumerate(events_list_dicts)
             if d["event_id"] == patch.event_id),
            None,
        )

        if idx is not None:
            events_list_dicts[idx] |= patch_clean

    # Persist events to database
    events_list_events = dicts_to_events(events_list_dicts)
    persist_events_to_db(os.environ["DUCKDB_PATH"], events_list_events)

    # Update state
    updated_state = {"events_list": events_list_events}
    return updated_state


def filter_events(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, List[Event]]:
    """
    Filter list of events based on user input on preferred event type.
    """

    pass


def finalize_output(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, str]:

    # Query LLM for final output message
    llm_client = create_llm_client(service=os.environ["LLM_SERVICE"])
    
    system_message = """
        You are a friendly guide that provides helpful event suggestions in German.
        Use the "Du"-form and not the "Sie"-form.
        """
    query_message = """
        Given the input provided as context, produce a text that presents the
        events in the list with basic information.
        If there are no events in the list, only state kindly that there are no
        suitable events (without offering any further assistance).
        """
    context=" ".join(str(e) for e in state.events_list)

    events_text = llm_client.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=query_message),
        HumanMessage(content=context)
    ])

    # Update state
    updated_state = {"output": events_text.content}
    return updated_state
