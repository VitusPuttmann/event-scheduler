"""
Handlers for the user input via a TelegramClient.
"""

from datetime import datetime

from scheduler_app.infra.telegram import TelegramClient


class MaxAttemptsExceeded(Exception):
    pass


def obtain_input_date(
    tg_client: TelegramClient,
    max_attempts: int = 3,
) -> tuple[str, int | None]:
    offset = tg_client.get_last_offset()

    for attempt in range(max_attempts):
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

        if attempt == max_attempts - 1:
            tg_client.send("Vielen Dank für Dein Interesse.")
            raise MaxAttemptsExceeded


def obtain_event_type(
    tg_client: TelegramClient,
    question_text: str,
    offset: int | None,
    valid_numbers: set[str],
    max_attempts: int = 3,
) -> tuple[str, int | None]:  # type: ignore[return]
    for attempt in range(max_attempts):
        tg_client.send(question_text)
        response, offset = tg_client.wait_for_reply(offset=offset)
        response = response.strip()

        if response in valid_numbers:
            return response, offset

        tg_client.send(
            f"Ungültige Eingabe. Bitte gib eine der folgenden Nummern an: {', '.join(sorted(valid_numbers))}"
        )

        if attempt == max_attempts - 1:
            tg_client.send("Vielen Dank für Dein Interesse.")
            raise MaxAttemptsExceeded
