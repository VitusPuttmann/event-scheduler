"""
Define data class for events.
"""

from dataclasses import dataclass
from datetime import datetime, date, time
from typing import List


@dataclass
class Event:
    event_type: str
    event_name: str
    event_artists: str | None = None
    event_date: date | None = None
    event_start_time: time | None = None
    event_end_time: time | None = None
    event_venue: str | None = None
    event_description: str | None = None


    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Event:
        def opt(key: str) -> str | None:
            return data.get(key) or None

        return cls(
            event_type=data["type"],
            event_name=data["name"],
            event_artists=opt("artists"),
            event_date=(
                datetime.strptime(data["date"], "%Y-%m-%d").date()
                if opt("date") else None
            ),
            event_start_time=(
                datetime.strptime(data["start"], "%H:%M").time()
                if opt("start") else None
            ),
            event_end_time=(
                datetime.strptime(data["end"], "%H:%M").time()
                if opt("end") else None
            ),
            event_venue=opt("venue"),
            event_description=opt("description")
        )
