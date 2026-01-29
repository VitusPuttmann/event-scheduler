"""
Invoke the LangGraph application.
"""

import argparse
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

import duckdb

from scheduler_graph.agent import graph
from scheduler_graph.database import ensure_table, EVENTS_TABLE


load_dotenv()

MAX_ATTEMPTS = 3

thread_id = "test_thread_001"
config = {
    "configurable": {"thread_id": thread_id}
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug-checkpoints",
        action="store_true",
        help="Print checkpoint count and logged LLM calls",
    )
    return parser.parse_args()

def init_db() -> None:
    db_path = os.environ["DUCKDB_PATH"]

    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(db_path) as con:
        ensure_table(con, EVENTS_TABLE)


def obtain_input_date() -> str:
    for attempt in range(MAX_ATTEMPTS):
        user_input = input(
            "Gib das gewünschte Datum im Format 'JJJJ-MM-TT' an: "
        ).strip()

        try:
            input_date = datetime.strptime(user_input, "%Y-%m-%d").date()
        except ValueError:
            print("Das Format des eingegebenen Datums ist ungültig.")
        else:    
            if input_date >= datetime.today().date():
                return user_input
            print(
                "Das Datum liegt in der Vergangenheit. Bitte gib ein anderes Datum an."
            )

        if attempt == MAX_ATTEMPTS - 1:
            print("Vielen Dank für Dein Interesse.")
            sys.exit(1)


if __name__ == "__main__":
    args = parse_args()

    user_input_date = obtain_input_date()
    initial_state = {
        "user_input_date": user_input_date
    }

    init_db()
    
    graph_result = graph.invoke(initial_state, config=config)
    output = graph_result["output"]
    print(output)

    if args.debug_checkpoints:
        history = list(graph.get_state_history(config))
        print(f"{len(history)} checkpoints recorded")
        try:
            print(graph_result["log_llmcalls"])
        except KeyError:
            print("No LLM calls logged.")
