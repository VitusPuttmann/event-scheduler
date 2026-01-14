"""
Define the state schema for the LangGraph application state.
"""

from pydantic import BaseModel, Field
from typing import List

from models.event import Event


class AgentState(BaseModel):
    user_input: str = Field(..., description="Text input from user")
    events: List[Event] = Field(default_factory=list, description="List of events processed throughout the graph")
    output: str = Field("", description="Processed event suggestions for user")
