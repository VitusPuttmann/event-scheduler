# Event Scheduler

Event Scheduler is a LangGraph-based Python application that finds and suggests
music events in Hamburg (currently focused on evening concerts).

It runs as a Telegram-connected workflow: the bot asks for a date and music
preference, the app collects and enriches events, and then sends back a final
recommendation message including a nearby public transport station and restaurant.

The project is primarily a learning project for LangGraph.

## Overview

- `🤖` Telegram bot interaction for user input/output
- `🕸️` Event discovery via crawling and parsing
- `🧠` LLM-driven augmentation and final response generation
- `🗄️` DuckDB persistence for event data
- `🔎` Optional web search support via Tavily

## Requirements

- Python 3.11+
- A Telegram bot token and chat id
- API keys for the configured LLM and web search provider

## Setup (Local Python)

1. Clone the repository:

```powershell
git clone https://github.com/VitusPuttmann/event-scheduler.git
cd event-scheduler
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Install dependencies and the application package:

```powershell
pip install -r requirements.txt
pip install -e .
```

Alternative single-step package install:

```powershell
pip install .
```

## Alternative Setup (Docker)

If you prefer containerized setup and execution, use Docker Compose.
See `README.Docker.md` for full details.

Quick start:

```powershell
docker compose up --build server
```

Run the CLI workflow in Docker:

```powershell
docker compose run --rm cli
```

## Configuration

Create `.env` from `.env.example` and set at least:

- `CONTACT_EMAIL`
- `DUCKDB_PATH` (default: `data/events.duckb`)
- `LLM_SERVICE="OpenAI"`
- `OPENAI_MODEL` and `OPENAI_API_KEY`
- `WEBSEARCH_SERVICE="Tavily"`
- `TAVILY_API_KEY`
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

## Run the app

```powershell
python -m scheduler_app.cli
```

Optional debug output for checkpoints and logged LLM calls:

```powershell
python -m scheduler_app.cli --debug-checkpoints
```

## Run tests

```powershell
pytest
```

## LangGraph config

`langgraph.json` is configured for this project:

- dependency root: `.`
- graph entrypoint: `./src/scheduler_app/graph/builder.py:graph`
- env file: `./.env`

## Visualize graph

Open and run the first code cell in:

- `scripts/graph.ipynb`
