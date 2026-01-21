"""
Schema for the LangGraph application state.
"""

from pydantic import BaseModel, Field
from typing import List

from models.event import Event


class AgentState(BaseModel):
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
        default_factory=list, description="Augmented list of events for the graph"
    )
    output: str = Field(
        "", description="Processed event suggestions for user"
    )
