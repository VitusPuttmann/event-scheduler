# To-Dos for the Event Scheduler

## Current

- Implement async / await for web search and LLM queries
- Ensure consistent input to LLM via dataclass
- Implement testing
- Implement logging
- Improve event search:
    - Check with_structured_output from LangChain
- Improve event selection:
    - Consider create_react_agent from LangGraph
    - Use interrupt or graph.update_state() for user feedback (consider feedback on available events for final selection of subset)
    - Consider establishing special connection (e.g., Phone) for user input
- Implement LLM-based reflection at some point
- Implement graceful degradation
- Consider implementing checkpointers for fault-tolerance and error recovery

## Files

### scheduler_graph/state.py
- Specify type hinting for events_raw
- Consider including validation (using field_validator and ValidationError)

### scheduler_graph/nodes.py
- Implement error handling for reading file and input to Event.from_dict()
- Improve automatic retrieval of events (ideally via API)

### scheduler_graph/edges.py
- Add actual edges or delete when not required

### scheduler_graph/main.py
- Implement error and type mismatch handling for user input

### scheduler_graph/tools.py
- Implement actual tools or delete when not required

### scheduler_graph/event.py
- Implement error handling for required fields of Event

### scheduler_graph/search.py
- Consider storage of raw and refined output data
- Consider implementing dataclass for search results

### scheduler_graph/llm.py
- Include model parameters in environment variables
- Include cost control

### langgraph.json
- Update file


# Questions

- Does the overall project structure make sense?
- Is the wrapping logic of the web search client reasonable? Is it problematic
    where the service_registry is placed?
