"""
Compilation of the LangGraph.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from scheduler_app.graph.state import AgentState
from scheduler_app.graph.nodes.find_events import find_events
from scheduler_app.graph.nodes.augment_events import augment_events
from scheduler_app.graph.nodes.load_events import load_events
from scheduler_app.graph.nodes.filter_events import filter_events
from scheduler_app.graph.nodes.finalize_output import finalize_output
from scheduler_app.graph.edges import check_data_availability


builder = StateGraph(AgentState)
checkpointer = InMemorySaver()

builder.add_node("find_events", find_events)
builder.add_node("augment_events", augment_events)
builder.add_node("load_events", load_events)
builder.add_node("filter_events", filter_events)
builder.add_node("finalize_output", finalize_output)

builder.add_conditional_edges(
    START,
    check_data_availability,
    {
        "data_not_available": "find_events",
        "data_available": "load_events",
    },
)
builder.add_edge("find_events", "augment_events")
builder.add_edge("augment_events", "filter_events")
builder.add_edge("load_events", "filter_events")
builder.add_edge("filter_events", "finalize_output")
builder.add_edge("finalize_output", END)

graph = builder.compile(checkpointer=checkpointer)
