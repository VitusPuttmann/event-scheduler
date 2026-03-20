"""
Invoke the LangGraph application.
"""

import argparse
from dotenv import load_dotenv
import os
import sys
from uuid import uuid4

from langgraph.types import Command
from scheduler_app.graph.builder import graph
from scheduler_app.infra.database import init_db
from scheduler_app.infra.telegram import TelegramClient
from scheduler_app.services.input_handlers import (
    MaxAttemptsExceeded,
    obtain_input_date,
    obtain_event_type
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug-checkpoints",
        action="store_true",
        help="Print checkpoint count and logged LLM calls",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    load_dotenv()

    db_path = os.environ["DUCKDB_PATH"]
    tg_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    tg_chat_id = int(os.environ["TELEGRAM_CHAT_ID"])

    with TelegramClient(tg_bot_token, tg_chat_id) as tg_client:
        config = {
            "configurable": {"thread_id": f"thread_{uuid4()}"}
        }

        try:
            user_input_date, offset = obtain_input_date(tg_client=tg_client)
        except MaxAttemptsExceeded:
            sys.exit(1)
        initial_state = {
            "user_input_date": user_input_date
        }

        init_db(db_path)

        result = graph.invoke(initial_state, config=config)
        while "__interrupt__" in result:
            intr = result["__interrupt__"][0]
            payload = intr.value

            question_text = payload["question"]
            for option in payload["data"]:
                question_text += "\n"
                question_text += option
            question_text += "\nDeine Auswahl:"

            user_choice, offset = obtain_event_type(
                tg_client=tg_client,
                question_text=question_text,
                offset=offset,
            )

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


if __name__ == "__main__":
    main()
