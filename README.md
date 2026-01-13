# Event Scheduler

This project develops an application that researches and selects events for
users. It is based on LangGraph.

At this stage, the project primarily serves as a learning exercise for LangGraph
and is not intended for deployment. Design flaws are therefore part of the process.

Requirements:
- Python 3.10+
-> See requirements.txt

Setup:
python -m venv .venv
.venv/Scripts/Activate.ps1
pip install -r requirements.txt

Run:
python main.py

Visualize Graph:
-> Run the code cell in the notebook graph.ipynb

Note:
- The scope for running the application is limited for now, and edge cases have
not been considered systematically so far. 
- Relevant output can be obtained by entering "2026-02-01" or "2026-02-01" as
user input.
