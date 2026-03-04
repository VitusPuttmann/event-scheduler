"""
Functions for obtaining user input via Telegram.
"""

from dotenv import load_dotenv
import os
import requests
import time


load_dotenv()

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"


def tg_send(chat_id: int, text: str) -> None:
    r = requests.post(
        f"{API_BASE}/sendMessage", json={"chat_id": chat_id, "text": text}
    )
    r.raise_for_status()


def tg_get_updates(offset: int | None = None, timeout: int = 30) -> dict:
    payload = {"timeout": timeout}
    if offset is not None:
        payload["offset"] = offset
    r = requests.get(
        f"{API_BASE}/getUpdates",
        params=payload,
        timeout=timeout + 15
    )
    r.raise_for_status()
    
    return r.json()


def tg_get_last_offset() -> int | None:
    data = tg_get_updates(offset=None, timeout=0)
    results = data.get("result", [])
    if not results:
        return None
    
    return results[-1]["update_id"] + 1


def wait_for_reply(
    chat_id: int, offset: int | None = None
) -> tuple[str, int | None]:
    while True:
        data = tg_get_updates(offset=offset, timeout=30)
        for upd in data.get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("message") or {}
            if msg.get("chat", {}).get("id") != chat_id:
                continue
            text = (msg.get("text") or "").strip()
            if text:
                return text, offset
        time.sleep(0.2)
