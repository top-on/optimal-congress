"""Tests for the models of the congress_optimizer app."""

from datetime import datetime
from uuid import uuid4

import pytest
from pytz import timezone

from optimal_congress.schema import Event, events_overlap

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


def test_event_hashing():
    """Assure that events with same id are equal."""
    event1 = Event(
        id=uuid4(),
        name="foo",
        slug="foo",
        track="foo",
        assembly="foo",
        room=None,
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
        description="bar",
        schedule_start=datetime(2023, 12, 27, 13, tzinfo=TZ_DE),
        schedule_end=datetime(2023, 12, 27, 15, tzinfo=TZ_DE),
    )

    assert event1 == event2
