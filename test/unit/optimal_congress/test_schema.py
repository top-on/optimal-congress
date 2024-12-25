"""Tests for the models of the congress_optimizer app."""

from datetime import datetime
from uuid import uuid4

import pytest
from pytz import timezone

from optimal_congress.schema import Event, EventLanguage, events_overlap, parse_language

TZ_DE = timezone("Europe/Berlin")


@pytest.mark.parametrize(
    "event1, event2, expected",
    [
        (
            Event(
                id=uuid4(),
                name="foo",
                slug="foo",
                track="foo",
                assembly="foo",
                room=None,
                language=["de"],
                description="foo",
                schedule_start=datetime(2023, 12, 27, 12, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 14, tzinfo=TZ_DE),
            ),
            Event(
                id=uuid4(),
                name="bar",
                slug="bar",
                track="bar",
                assembly="bar",
                room=None,
                language=["de"],
                description="bar",
                schedule_start=datetime(2023, 12, 27, 13, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 15, tzinfo=TZ_DE),
            ),
            True,
        ),
        (
            Event(
                id=uuid4(),
                name="foo",
                slug="foo",
                track="foo",
                assembly="foo",
                room=None,
                language=["de"],
                description="foo",
                schedule_start=datetime(2023, 12, 27, 12, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 14, tzinfo=TZ_DE),
            ),
            Event(
                id=uuid4(),
                name="bar",
                slug="bar",
                track="bar",
                assembly="bar",
                room=None,
                language=["de"],
                description="bar",
                schedule_start=datetime(2023, 12, 27, 15, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 17, tzinfo=TZ_DE),
            ),
            False,
        ),
        (
            Event(
                id=uuid4(),
                name="foo",
                slug="foo",
                track="foo",
                assembly="foo",
                room=None,
                language=["de"],
                description="foo",
                schedule_start=datetime(2023, 12, 27, hour=12, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 13, tzinfo=TZ_DE),
            ),
            Event(
                id=uuid4(),
                name="bar",
                slug="bar",
                track="bar",
                assembly="bar",
                room=None,
                language=["de"],
                description="bar",
                schedule_start=datetime(2023, 12, 27, 13, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 14, tzinfo=TZ_DE),
            ),
            False,
        ),
    ],
)
def test_events_overlap(event1: Event, event2: Event, expected: bool):
    """Test overlapping check."""

    result1 = events_overlap(event1, event2)
    result2 = events_overlap(event2, event1)

    assert result1 == result2
    assert result1 == expected


def test_event_is_equal():
    """Assure that events with same id are equal."""
    event1 = Event(
        id=uuid4(),
        name="foo",
        slug="foo",
        track="foo",
        assembly="foo",
        room=None,
        language=["de"],
        description="foo",
        schedule_start=datetime(2023, 12, 27, 12, tzinfo=TZ_DE),
        schedule_end=datetime(2023, 12, 27, 14, tzinfo=TZ_DE),
    )
    event2 = Event(
        id=event1.id,
        name="bar",
        slug="bar",
        track="bar",
        assembly="bar",
        room=None,
        language=["de"],
        description="bar",
        schedule_start=datetime(2023, 12, 27, 13, tzinfo=TZ_DE),
        schedule_end=datetime(2023, 12, 27, 15, tzinfo=TZ_DE),
    )

    assert event1 == event2


@pytest.mark.parametrize(
    "event1, event2",
    [
        (
            Event(
                id=uuid4(),
                name="foo",
                slug="foo",
                track="foo",
                assembly="foo",
                room=None,
                description="foo",
                schedule_start=datetime(2023, 12, 27, 15, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 17, tzinfo=TZ_DE),
            ),
            Event(
                id=uuid4(),
                name="bar",
                slug="bar",
                track="bar",
                assembly="bar",
                room=None,
                description="bar",
                schedule_start=datetime(2023, 12, 27, 15, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 17, tzinfo=TZ_DE),
            ),
        ),
    ],
)
def test_event_not_equal(event1: Event, event2: Event):
    """Assure that events with different id are not equal."""
    assert event1 != event2


def test_parse_language():
    """Test language parsing."""
    assert parse_language(None) is None
    assert parse_language("de") == ["de"]
    assert parse_language("de, en") == ["de", "en"]
    assert parse_language(["en", "de"]) == ["en", "de"]


@pytest.mark.parametrize(
    "language_input, expected",
    [
        (None, None),
        ("de", ["de"]),
        ("de, en", ["de", "en"]),
        (["en", "de"], ["en", "de"]),
    ],
)
def test_event_parse_language(
    language_input: list[EventLanguage] | str | None,
    expected: list[EventLanguage] | None,
):
    """Test instantiation of event, with language parsing."""
    event = Event(
        id=uuid4(),
        name="foo",
        slug="foo",
        track="foo",
        assembly="foo",
        room=None,
        language=language_input,  # type: ignore
        description="foo",
        schedule_start=datetime(2023, 12, 27, 12, tzinfo=TZ_DE),
        schedule_end=datetime(2023, 12, 27, 14, tzinfo=TZ_DE),
    )

    assert event.language == expected
