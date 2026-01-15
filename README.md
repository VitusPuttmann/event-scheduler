# Event Scheduler

This project develops an application that researches and selects events for its
users. It is based on LangGraph.

At this stage, the project primarily serves as a learning exercise for LangGraph
and is not intended for deployment. Design flaws are therefore part of the process.

## Requirements

- Python 3.14  
- See requirements.txt

## Setup

python -m venv .venv  
.venv/Scripts/Activate.ps1  
pip install -r requirements.txt

## Prepare config

- Create .env based on .env.example
- Use: LLM_SERVICE="OpenAI"
- Use: WEBSEARCH_SERVICE="Tavily"

## Run

python main.py

## Visualize graph

- Run the first code cell in the notebook graph.ipynb
