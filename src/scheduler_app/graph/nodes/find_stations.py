"""
Node for finding nearby public transport stations.
"""

from datetime import datetime
import json
import os
from pydantic import BaseModel, Field, ValidationError
from typing import Any, List, Optional
from uuid import uuid4

from langchain_core.runnables import RunnableConfig

from scheduler_app.graph.state import AgentState
from scheduler_app.app_logging.log_llm import LLMCallEvent, log_llmcall
from scheduler_app.graph.tools.web_search import search_web
from scheduler_app.infra.llm import create_llm_client


MAX_RETRIES = 3


class StationSearchResult(BaseModel):
    stations: List[str] = Field(
        default_factory=list,
        description="Nearby public transport stations, each as one short text line",
    )


def find_stations(
    state: AgentState, config: Optional[RunnableConfig] = None
) -> dict[str, Any]:
    """
    Find public transport stations near an event venue via LLM + web search.
    """

    if not state.events_list_filtered:
        return {"places_near_venue": []}

    selected_event = state.events_list_filtered[0]

    llm_client, token_counter = create_llm_client(
        service=os.environ["LLM_SERVICE"],
        dollars_already_spent=state.dollars_expended,
        budget_exceeded=state.budget_exceeded
    )
    llm_client_with_tool = llm_client.bind_tools([search_web])
    locator = llm_client_with_tool.with_structured_output(StationSearchResult) # pyright: ignore[reportAttributeAccessIssue]

    system_message = """
        You suggest public transport stations near an event venue.
        Consider train, subway and bus.
        Use the search_web tool to gather current information.
        Prefer places in walking distance.
        Keep each suggestion concise and factual.
        """
    query_message = """
        Return up to 3 suggestions in German.
        Each list item should include station name and transport type
        (i.e., train, subway or bus).
        """
    context = json.dumps(
        {
            "event_venue": selected_event.event_venue
        },
        ensure_ascii=False,
    )

    msg = [
        ("system", system_message),
        ("user", query_message),
        ("user", context),
    ]

    suggestions: List[str] = []
    attempts = 0
    for attempt in range(MAX_RETRIES):
        if token_counter.budget_exceeded:
            break

        attempts += 1
        try:
            llm_output: StationSearchResult = locator.invoke(
                msg, config={"callbacks": [token_counter]}
            )
            suggestions = llm_output.stations[:3]
            break
        except ValidationError:
            if attempt == MAX_RETRIES - 1:
                suggestions = []

    llmcall_log_entry: LLMCallEvent = log_llmcall(
        provider=os.environ["LLM_SERVICE"],
        messages=msg,
        output=suggestions,
        attempts=attempts,
        node="find_stations",
        timestamp=str(datetime.now().isoformat()),
        request_id=str(uuid4()),
    )

    return {
        "places_near_venue": suggestions,
        "log_llmcalls": (state.log_llmcalls or []) + [llmcall_log_entry],
        "dollars_expended": token_counter.dollars_spent_this_node,
        "budget_exceeded": token_counter.budget_exceeded,
    }