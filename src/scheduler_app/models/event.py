"""
Classes for events and event patches.
"""

from __future__ import annotations

import hashlib
from datetime import date
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional, List, Literal


EventType = Literal[
    "Klassik",
    "Jazz, Blues, Funk",
    "Rock, Indie, Metal",
    "HipHop, RnB, Soul",
    "Elektro, Techno, House",
    "Pop, Schlager",
]

@dataclass
class Event:
    event_id: str
    event_name: str
    event_date: date
    event_time: str
    event_venue: str | None = None
    event_type: str | None = None
    event_description: str | None = None
    event_url: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Event:
        def opt(key: str) -> str | None:
            return data.get(key) or None

        event_id = data.get("event_id") or hashlib.sha256(
            f"{data['event_name']}|{data['event_date']}|{data['event_time']}"
            .encode("utf-8")
        ).hexdigest()

        return cls(
            event_id=event_id,
            event_name=data["event_name"],
            event_date=date.fromisoformat(data["event_date"]),
            event_time=data["event_time"],
            event_venue=opt("event_venue"),
            event_type=opt("event_type"),
            event_description=opt("event_description"),
            event_url=opt("event_url"),
        )

    def __str__(self) -> str:
        return (
            f"{self.event_name}, {self.event_date}, "
            f"{self.event_time}, {self.event_venue}, {self.event_type}, "
            f"{self.event_description}, {self.event_url}."
        )

    def to_db_tuple(self) -> tuple:
        return (
            self.event_id,
            self.event_name,
            self.event_date,
            self.event_time,
            self.event_venue,
            self.event_type,
            self.event_description,
            self.event_url,
        )


class EventPatch(BaseModel):
    event_id: str
    event_type: Optional[EventType] = None
    event_description: Optional[str] = None


class AugmentationResult(BaseModel):
    patches: List[EventPatch]
