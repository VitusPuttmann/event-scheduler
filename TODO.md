# To-Dos for the Event Scheduler

## Current

- Split the tavily.py
- Remove load_dotenv() from telegram.py
- Update langgraph.json
- Update pyproject.toml and requirements.txt
- Update README.md

- Revise the entire Event dataclass with a view to required transformations throughout the graph
- Implement LLM-based reflection at some point
- Implement graceful degradation
- Improve handling of user input for event selection


## Files

### main.py
- Consider shifting functions for input validation and database initiation to
    separate scripts

### scheduler_graph/state.py


### scheduler_graph/agent.py


### scheduler_graph/nodes.py
- Check possibilities for shifting functions and logic to separate scripts
- Improve automatic retrieval of events (ideally via API)

### scheduler_graph/edges.py
- Adapt routing logic to creation of database at graph start

### scheduler_graph/tools.py
- Adapt call limiter to restrict explicity to one per loop iteration in node

### models/event.py
- Reconsider entire class structure given required transformations
- Implement error handling

### scheduler_graph/llm.py
- Include cost control
- Check additional model parameters for relevant options

### scheduler_graph/crawler.py
- Account for limits of scraping and implement safeguards via rate-limit and back off on errors
- Implement that results requiring additional website loads are included
    - Consider create_react_agent from LangGraph
- Consider including additional fields from the html
- Consider extending it to other websites

### scheduler_graph/parser.py
- Check parsing logic in detail

### scheduler_graph/database.py
- Address security of f-strings

### ai_logging/log_llm.py


### langgraph.json
- Update file


## Information on Database

Dates covered in local database:
2026-02-20
2026-02-21
2026-02-22
2026-02-23
2026-02-24
2026-02-25
2026-02-26
2026-03-09 (no events)
2026-03-13 (no events)
2026-03-14 (events)
2026-03-15 (no events)
2026-03-16 (events)
2026-03-17 (event)
