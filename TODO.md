# To-Dos for the Event Scheduler

Date for testing in local database: 2026-03-19 (events)

- Final check for functionality, security, and refactoring possibilities

## Current

- Address security of f-strings in database
- Deal with environment variables in Docker
- Implement requests.Session() for Telegram and streaming event updates during execution
- Shift functions for input validation from cli.py to separate scripts
- Revise the Event dataclass with a view to required transformations throughout the graph

## Additionl

- Improve handling of user input for event selection
- Implement cost control and graceful degradation for LLM
- Improve automatic retrieval of events (ideally via API)
- Expand crawling
    - Account for limits of scraping and implement safeguards via rate-limit and back off on errors
    - Implement that results requiring additional website loads are included (consider create_react_agent from LangGraph)
    - Consider including additional fields from the HTML
    - Consider extending it to other websites
