"""
Unit tests for filtering events.
"""

from datetime import date, time

from scheduler_app.graph.state import AgentState
from scheduler_app.models.event import Event
from scheduler_app.graph.nodes.filter_events import filter_events


def _make_event(event_id: str, event_type: str) -> Event:
    return Event(
        event_id=event_id,
        event_name=f"Event {event_id}",
        event_date=date(2026, 2, 20),
        event_time=time(20, 0),
        event_venue="Venue",
        event_type=event_type,
        event_description="Desc",
        event_url="https://example.com",
    )


def test_filter_events_returns_at_most_one_matching_event(monkeypatch):
    state = AgentState(
        user_input_date="2026-02-20",
        user_input_type="",
        events_list=[
            _make_event("1", "Klassik"),
            _make_event("2", "Klassik"),
            _make_event("3", "Jazz, Blues, Funk"),
        ],
        output="",
    )

    monkeypatch.setattr(
        "scheduler_app.graph.nodes.filter_events.interrupt",
        lambda payload: "1",
    )

    result = filter_events(state)

    assert "events_list_filtered" in result
    assert len(result["events_list_filtered"]) == 1
    assert result["events_list_filtered"][0].event_id == "1"
