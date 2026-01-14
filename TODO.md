# To-Dos for the event scheduler

## Current

. Implement two AI tools (event search, consider using Tavily search tool, and selection or output processing)
. Implement testing
. Implement logging
. Extend initial user input in main.py to include interests
. Establish Telegram connection for user input or output
. Establish automated connection for event input (remove events.csv)
. Consider including validation in state.py (using field_validator and ValidationError)
. Implement graceful degradation
. Implement config schema
    from typing_extensions import TypedDict
    from langchain_core.runnables import RunnableConfig
    class GraphConfigSchema(TypedDict):
        llm_model_name: str
        temperature: float
    builder = StateGraph(MyState, config_schema=GraphConfigSchema)

. Relevant design issues
    . Use of operator.add and add_messages
    . Use async and await
    . Use try-except
    . Use checkpointers for fault-tolerance and error recovery

## Files

### my_graph/state.py
. Develop state schema further

### my_graph/nodes.py
. Implement error handling for reading file and input to Event.from_dict()
. Implement automatic retrieval of events (either API or AI)
. Expand filtering to include user interests (based on expanded initial input)
. Deal with potential appearance of None in output text

### my_graph/edges.py
. Add actual edges or delete when not required

### my_graph/main.py
. Implement error and type mismatch handling for user input

### my_graph/tools.py
. Implement actual tools or delete when not required

### event.py
. Implement error handling for required fields of Event
. Consider defining class Artist and changing related field of Event

### .env.example
. Implement example

### langgraph.json
. Update file
