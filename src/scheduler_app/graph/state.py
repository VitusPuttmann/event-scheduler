"""
Schema for the LangGraph application state.
"""

import operator
from pydantic import BaseModel, Field
from typing import Annotated, Optional, List

from scheduler_app.models.event import Event
from scheduler_app.app_logging.log_llm import LLMCallEvent


def _or(a: bool, b: bool) -> bool:
    return a or b


class AgentState(BaseModel):
    # For main function
    user_input_date: str = Field(
        ..., description="Text input from user on preferred date"
    )
    user_input_type: str = Field(
        "", description="Text input from user on preferred event type"
    )
    events_list: List[Event] = Field(
        default_factory=list, description="Augmented list of events"
    )
    events_list_filtered: List[Event] = Field(
        default_factory=list, description="Augmented list of events filtered based on user input"
    )
    places_near_venue: Annotated[List[str], operator.add] = Field(
        default_factory=list,
        description="Public transport station and restaurant suggestion near the event venue"
    )
    output: str = Field(
        "", description="Processed event suggestions for user"
    )

    # For budget control
    dollars_expended: Annotated[float, operator.add] = Field(
        0, description="Amount of dollars expended for LLM calls"
    )
    budget_exceeded: Annotated[bool, _or] = Field(
        False, description="Flag for whether budget limit is exceeded"
    )

    # For logging
    log_llmcalls: Annotated[Optional[List[LLMCallEvent]], operator.add] = Field(
        default_factory=list,
        description="Overview on LLM calls with inputs/outputs and metadata"
    )