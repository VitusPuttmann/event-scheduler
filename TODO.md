# To-Dos for the Event Scheduler

Date for testing in local database: 2026-03-19 (events)

- Revise the entire Event dataclass with a view to required transformations throughout the graph
- Implement requests.Session() for Telegram and streaming event updates during execution
- Shift functions for input validation from cli.py to separate scripts
- Address security of f-strings in database
- Implement cost control and graceful degradation for LLM
- Improve handling of user input for event selection
- Improve automatic retrieval of events (ideally via API)
- Expand crawling
    - Account for limits of scraping and implement safeguards via rate-limit and back off on errors
    - Implement that results requiring additional website loads are included (consider create_react_agent from LangGraph)
    - Consider including additional fields from the html
    - Consider extending it to other websites
