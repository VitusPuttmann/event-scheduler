"""
Invoke the LangGraph application.
"""

import argparse
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

from langgraph.types import Command
from scheduler_app.graph.builder import graph
from scheduler_app.infra.database import init_db
from scheduler_app.infra.telegram import TelegramClient


thread_id = "test_thread_001"
config = {
    "configurable": {"thread_id": thread_id}
}


load_dotenv()

MAX_ATTEMPTS = 3

DB_PATH = os.environ["DUCKDB_PATH"]

TG_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TG_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

tg_client = TelegramClient(TG_BOT_TOKEN, TG_CHAT_ID)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug-checkpoints",
        action="store_true",
        help="Print checkpoint count and logged LLM calls",
    )
    return parser.parse_args()


def obtain_input_date() -> tuple[str, int | None]:
    offset = tg_client.get_last_offset()

    for attempt in range(MAX_ATTEMPTS):
        tg_client.send(
            "Gib das gewünschte Datum im Format 'JJJJ-MM-TT' an:"
        )
        user_input, offset = tg_client.wait_for_reply(offset=offset)
        user_input = user_input.strip()

        try:
            input_date = datetime.strptime(user_input, "%Y-%m-%d").date()
        except ValueError:
            tg_client.send(
                "Das Format des eingegebenen Datums ist ungültig."
            )
        else:    
            if input_date >= datetime.today().date():
                return user_input, offset
            tg_client.send(
                "Das Datum liegt in der Vergangenheit. Bitte gib ein anderes Datum an."
            )

        if attempt == MAX_ATTEMPTS - 1:
            tg_client.send("Vielen Dank für Dein Interesse.")
            sys.exit(1)


def obtain_event_type(
    question_text: str, offset: int | None
) -> tuple[str, int | None]:
    tg_client.send(question_text)

    response, offset = tg_client.wait_for_reply(offset=offset)

    return response, offset


if __name__ == "__main__":
    args = parse_args()
    offset = tg_client.get_last_offset()

    user_input_date, offset = obtain_input_date()
    initial_state = {
        "user_input_date": user_input_date
    }

    init_db(DB_PATH)
    
    result = graph.invoke(initial_state, config=config)
    while "__interrupt__" in result:
        intr = result["__interrupt__"][0]
        payload = intr.value

        question_text = payload["question"]
        for option in payload["data"]:
            question_text += "\n"
            question_text += option
        question_text += "\nDeine Auswahl:"

        user_choice, offset = obtain_event_type(question_text, offset)

        result = graph.invoke(
            Command(resume=user_choice),
            config=config
        )

    output = result["output"]
    
    tg_client.send(output)

    if args.debug_checkpoints:
        history = list(graph.get_state_history(config))
        print(f"{len(history)} checkpoints recorded")
        try:
            print(result["log_llmcalls"])
        except KeyError:
            print("No LLM calls logged.")
