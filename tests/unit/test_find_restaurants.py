"""
Unit tests for the find restaurants node.
"""

from datetime import date, time

from scheduler_app.graph.state import AgentState
from scheduler_app.models.event import Event
from scheduler_app.graph.nodes.find_restaurants import find_restaurants


def _make_event(event_id: str) -> Event:
    return Event(
        event_id=event_id,
        event_name=f"Event {event_id}",
        event_date=date(2026, 3, 19),
        event_time=time(20, 0),
        event_venue="Elbphilharmonie",
        event_type="Klassik",
        event_description="Desc",
        event_url="https://example.com/event",
    )


class _FakeLocator:
    def __init__(self, restaurants):
        self._restaurants = restaurants

    def invoke(self, msg):
        from scheduler_app.graph.nodes.find_restaurants import RestaurantSearchResult

        return RestaurantSearchResult(restaurants=self._restaurants)


class _FakeLLM:
    def __init__(self, restaurants):
        self._restaurants = restaurants

    def bind_tools(self, tools):
        return self

    def with_structured_output(self, model):
        return _FakeLocator(self._restaurants)


def test_find_restaurants_returns_empty_when_no_selected_event():
    state = AgentState(
        user_input_date="2026-03-19",
        user_input_type="",
        events_list_filtered=[],
        output="",
    )

    result = find_restaurants(state)

    assert result == {"restaurants_near_event": []}


def test_find_restaurants_returns_up_to_three_suggestions(monkeypatch):
    monkeypatch.setenv("LLM_SERVICE", "OpenAI")
    monkeypatch.setattr(
        "scheduler_app.graph.nodes.find_restaurants.create_llm_client",
        lambda service: _FakeLLM(
            [
                "Restaurant A - 4 Minuten zu Fuss, gute Bewertungen.",
                "Restaurant B - Direkt am Venue, italienische Küche.",
                "Restaurant C - Nahe U-Bahn, schnelle Küche.",
                "Restaurant D - Ebenfalls in der Nähe.",
            ]
        ),
    )

    state = AgentState(
        user_input_date="2026-03-19",
        user_input_type="",
        events_list_filtered=[_make_event("1")],
        output="",
    )

    result = find_restaurants(state)

    assert len(result["restaurants_near_event"]) == 3
    assert result["restaurants_near_event"][0].startswith("Restaurant A")
    assert result["log_llmcalls"][0]["node"] == "find_restaurants"
