"""
Node for finalizing the output.
"""

import os
from typing import Optional

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage

from scheduler_app.graph.state import AgentState
from scheduler_app.infra.llm import create_llm_client


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
        event with basic information.
        If public transport station and restaurant recommendations are provided,
        include one station and one restaurant recommendation in a short section
        for places near the venue.
        If there is no event listed, only state kindly that there are no
        suitable events (without offering any further assistance).
        """
    context = (
        f"events={state.events_list_filtered}; "
        f"places_near_venue={state.places_near_venue}"
    )

    events_text = llm_client.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=query_message),
        HumanMessage(content=context)
    ])

    # Update state
    updated_state = {"output": events_text.content}
    return updated_state
