"""
Classes for events and event patches.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, date, time
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional, List, Literal


@dataclass
class Event:
    event_id: str
    event_name: str
    event_date: date
    event_time: time
    event_venue: str | None = None
    event_type: str | None = None
    event_description: str | None = None
    event_url: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Event:
        def opt(key: str) -> str | None:
            return data.get(key) or None

        return cls(
            event_id = hashlib.sha256(
                f"{data['event_name']}|{data['event_date']}|{data['event_time']}"
                .encode("utf-8")
            ).hexdigest(),
            event_name=data["event_name"],
            event_date=datetime.strptime(data["event_date"], "%d.%m.%Y").date(),
            event_time=datetime.strptime(data["event_time"], "%H:%M").time(),
            event_venue=opt("event_venue"),
            event_type=opt("event_type"),
            event_description=opt("event_description"),
            event_url=opt("event_url")
        )

    def __str__(self) -> str:
        return (
            f"{self.event_name}, {self.event_date}, "
            f"{self.event_time}, {self.event_venue}, {self.event_type}, "
            f"{self.event_description}, {self.event_url}."
        )

    def to_tuple(self) -> tuple:
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


EventType = Literal[
    "Klassik",
    "Jazz, Blues, Funk",
    "Rock, Indie, Metal",
    "HipHop, RnB, Soul",
    "Elektro, Techno, House",
    "Pop, Schlager",
]

class EventPatch(BaseModel):
    event_id: str
    event_type: Optional[EventType] = None
    event_description: Optional[str] = None

class AugmentationResult(BaseModel):
    patches: List[EventPatch]


def dicts_to_events(events_list_dicts: list[dict]) -> List[Event]:
    events: List[Event] = []

    for d in events_list_dicts:
        events.append(
            Event(
                event_id=d["event_id"],
                event_name=d["event_name"],
                event_date=d["event_date"],
                event_time=time.fromisoformat(d["event_time"]),
                event_venue=d.get("event_venue"),
                event_type=d.get("event_type"),
                event_description=d.get("event_description"),
                event_url=d.get("event_url"),
            )
        )

    return events
