"""
Unit tests for the html parser.
"""

from pathlib import Path
from datetime import datetime, date, time

from scheduler_graph.parser import extract_events


FIXTURE_DIR = Path(__file__).parent.parent / "fixtures"
SAMPLE_HTML = FIXTURE_DIR / "events_calendar_sample.html"


def test_extract_events_returns_nonempty_list():
    html = SAMPLE_HTML.read_text(encoding="utf-8")
    page_url = "https://www.hamburg-tourism.de/sehen-erleben/veranstaltungen/veranstaltungskalender/"

    events = extract_events(html, page_url)
    
    assert isinstance(events, list)
    assert len(events) > 0


def test_extract_events_first_event_has_correct_content():
    html = SAMPLE_HTML.read_text(encoding="utf-8")
    page_url = "https://www.hamburg-tourism.de/sehen-erleben/veranstaltungen/veranstaltungskalender/"

    events = extract_events(html, page_url)
    e0 = events[0]

    assert getattr(e0, "event_name") == "Warkings + Visions Of Atlantis - Pirates & Kings Tour 2026"
    assert getattr(e0, "event_date") == datetime.strptime("20.02.2026", "%d.%m.%Y").date()
    assert getattr(e0, "event_time") == datetime.strptime("18:45", "%H:%M").time()
    assert getattr(e0, "event_url", None)
    assert str(getattr(e0, "event_url")).startswith("http")
