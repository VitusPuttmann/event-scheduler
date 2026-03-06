"""
Telegram client.
"""

import requests
import time


class TelegramClient:
    def __init__(self, bot_token: str, chat_id: int):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_base = f"https://api.telegram.org/bot{bot_token}"

    def send(self, text: str) -> None:
        r = requests.post(
            f"{self.api_base}/sendMessage",
            json={"chat_id": self.chat_id, "text": text},
            timeout=30,
        )
        r.raise_for_status()

    def get_updates(self, offset: int | None = None, timeout: int = 30) -> dict:
        payload = {"timeout": timeout}
        if offset is not None:
            payload["offset"] = offset
        
        r = requests.get(
            f"{self.api_base}/getUpdates",
            params=payload,
            timeout=timeout + 15
        )
        r.raise_for_status()

        return r.json()

    def get_last_offset(self) -> int | None:
        data = self.get_updates(offset=None, timeout=0)
        results = data.get("result", [])
    
        if not results:
            return None
        return results[-1]["update_id"] + 1

    def wait_for_reply(
        self, offset: int | None = None
    ) -> tuple[str, int]:
        while True:
            data = self.get_updates(offset=offset, timeout=30)
            for upd in data.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message") or {}
                if msg.get("chat", {}).get("id") != self.chat_id:
                    continue
                text = (msg.get("text") or "").strip()
                if text:
                    return text, offset
            time.sleep(0.2)
