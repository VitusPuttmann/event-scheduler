# To-Dos for the Event Scheduler

- Improve handling of user input for event selection
- Implement cost control and graceful degradation for LLM
- Improve automatic retrieval of events (ideally via API)
- Expand crawling
    - Account for limits of scraping and implement safeguards via rate-limit and back off on errors
    - Implement that results requiring additional website loads are included (consider create_react_agent from LangGraph)
    - Consider including additional fields from the HTML
    - Consider extending it to other websites
