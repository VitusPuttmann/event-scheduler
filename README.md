# Event Scheduler

Event Scheduler is a LangGraph-based Python application that finds and suggests
music events in Hamburg (currently focused on evening concerts).

The project is primarily a learning project for LangGraph.

## Requirements

- Python 3.11+
- A Telegram bot token and chat id
- API keys for the configured LLM and web search provider

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

If you prefer a single-step package install instead of `requirements.txt`:

```powershell
pip install .
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
