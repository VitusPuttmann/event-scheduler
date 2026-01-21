"""
Unit test for the event dataclass.
"""

from datetime import date, time

from models.event import Event


def test_from_dict_parses_required_fields():
    data = {
        "event_name": "Test Event Name",
        "event_date": "02.01.2000",
        "event_time": "20:00"
    }

    e = Event.from_dict(data)

    assert e.event_name == "Test Event Name"
    assert e.event_date == date(2000, 1, 2)
    assert e.event_time == time(20, 0)


def test_from_dict_sets_optional_fields_to_none_when_missing():
    data = {
        "event_name": "Test Event Name",
        "event_date": "02.01.2000",
        "event_time": "20:00"
    }

    e = Event.from_dict(data)

    assert e.event_venue is None
    assert e.event_type is None
    assert e.event_description is None


def test_from_dict_sets_optional_fields_when_present():
    data = {
        "event_name": "Test Event Name",
        "event_date": "02.01.2000",
        "event_time": "20:00",
        "event_venue": "Test Venue",
        "event_type": "Test Type",
        "event_description": "A test description."
    }

    e = Event.from_dict(data)

    assert e.event_venue == "Test Venue"
    assert e.event_type == "Test Type"
    assert e.event_description == "A test description."


def test_str_contains_key_information():
    e = Event(
        event_id="id",
        event_name="Test Event Name",
        event_date=date(2000, 1, 2),
        event_time=time(20, 0),
        event_venue="Test Venue",
        event_type="Test Type",
        event_description="A test description."
    )

    s = str(e)

    assert "Test Event Name" in s
    assert "2000-01-02" in s
    assert "20:00:00" in s
    assert "Test Venue" in s
    assert "Test Type" in s
    assert "A test description." in s
