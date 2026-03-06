"""
Schema for the LangGraph application state.
"""

from pydantic import BaseModel, Field
from typing import Annotated, Optional, List
from operator import add

from scheduler_app.models.event import Event
from scheduler_app.app_logging.log_llm import LLMCallEvent


class AgentState(BaseModel):
    # For main function
    user_input_date: str = Field(
        ..., description="Text input from user on preferred date"
    )
    user_input_type: str = Field(
        "", description="Text input from user on preferred event type"
    )
    events_raw: List[Event] = Field(
        default_factory=list, description="Unaugmented output of web search for events"
    )
    events_list: List[Event] = Field(
        default_factory=list, description="Augmented list of events"
    )
    events_list_filtered: List[Event] = Field(
        default_factory=list, description="Augmented list of events filtered based on user input"
    )
    places_near_venue: Annotated[List[str], add] = Field(
        default_factory=list,
        description="Public transport station and restaurant suggestion near the event venue"
    )
    output: str = Field(
        "", description="Processed event suggestions for user"
    )

    # For logging
    log_llmcalls: Annotated[Optional[List[LLMCallEvent]], add] = Field(
        default_factory=list,
        description = "Overview on LLM calls with inputs/outputs and metadata"
    )
