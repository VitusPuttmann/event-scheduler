"""
Schema for the LangGraph application state.
"""

from pydantic import BaseModel, Field
from typing import Optional, List

from models.event import Event
from ai_logging.log_llm import LLMCallEvent


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
    output: str = Field(
        "", description="Processed event suggestions for user"
    )

    # For logging
    log_llmcalls: Optional[List[LLMCallEvent]] = Field(
        default_factory=list,
        description = "Overview on LLM calls with inputs/outputs and metadata"
    )
