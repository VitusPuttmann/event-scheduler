"""
Compile the LangGraph.
"""

from langgraph.graph import StateGraph, START, END

from scheduler_graph.state import AgentState
from scheduler_graph.nodes import find_events, filter_events, finalize_output


builder = StateGraph(AgentState)

builder.add_node("find_events", find_events)
builder.add_node("filter_events", filter_events)
builder.add_node("finalize_output", finalize_output)
builder.add_edge(START, "find_events")
builder.add_edge("find_events", "filter_events")
builder.add_edge("filter_events", "finalize_output")
builder.add_edge("finalize_output", END)

graph = builder.compile()
