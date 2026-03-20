"""
Node for augmenting events.
"""

import os
from datetime import datetime
from uuid import uuid4
import json
from pydantic import ValidationError
from typing import List, Optional

from langchain_core.runnables import RunnableConfig

from scheduler_app.models.event import Event, AugmentationResult
from scheduler_app.app_logging.log_llm import LLMCallEvent, log_llmcall
from scheduler_app.graph.state import AgentState
from scheduler_app.graph.tools.web_search import search_web
from scheduler_app.infra.database import persist_events_to_db, load_events_from_db
from scheduler_app.infra.llm import create_llm_client


MAX_RETRIES = 3


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

    llm_client_with_tool = llm_client.bind_tools([search_web])
    augmenter = llm_client_with_tool.with_structured_output(AugmentationResult)

    system_message = """
        You augment information on events. Only fill event_type and
        event_description.
        Infer event_type from the event_name and event_description. Do not
        invent facts.
        """
    query_message = """
        Return patches.
        """
    context = json.dumps(events_list_dicts, ensure_ascii=False)

    msg = [
        ("system", system_message),
        ("user", query_message),
        ("user", context),
    ]

    patches = []
    attempts = 0
    for attempt in range(MAX_RETRIES):
        attempts += 1

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
    events_list_events = [Event.from_dict(d) for d in events_list_dicts]
    persist_events_to_db(os.environ["DUCKDB_PATH"], events_list_events)

    # Log information on LLM call
    llmcall_log_entry: LLMCallEvent = log_llmcall(
        provider = os.environ["LLM_SERVICE"],
        messages = msg,
        output = patches,
        attempts = attempts,
        node = "augment_events",
        timestamp = str(datetime.now().isoformat()),
        request_id = str(uuid4())
    )

    # Update state
    updated_state = {
        "events_list": events_list_events,
        "log_llmcalls": state.log_llmcalls + [llmcall_log_entry]
    }
    return updated_state
