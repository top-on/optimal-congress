"""Test optimization functions."""

from datetime import datetime
from uuid import uuid4

from pytz import timezone

from congress_optimizer.models import Event, Rating
from congress_optimizer.optimize import optimize_schedule

TZ_DE = timezone("Europe/Berlin")


def test_optimize_schedule() -> None:
    # INPUT
    # event 'bar' overlaps with both other events
    events: list[Event] = [
        Event(
            id=uuid4(),
            name="foo",
            slug="foo",
            track="foo",
            assembly="foo",
            room=None,
            description="foo",
            schedule_start=datetime(2023, 12, 27, 7, tzinfo=TZ_DE),
            schedule_end=datetime(2023, 12, 27, 9, tzinfo=TZ_DE),
        ),
        Event(
            id=uuid4(),
            name="bar",
            slug="bar",
            track="bar",
            assembly="bar",
            room=None,
            description="bar",
            schedule_start=datetime(2023, 12, 27, 8, tzinfo=TZ_DE),
            schedule_end=datetime(2023, 12, 27, 10, tzinfo=TZ_DE),
        ),
        Event(
            id=uuid4(),
            name="baz",
            slug="baz",
            track="baz",
            assembly="baz",
            room=None,
            description="baz",
            schedule_start=datetime(2023, 12, 27, 9, tzinfo=TZ_DE),
            schedule_end=datetime(2023, 12, 27, 12, tzinfo=TZ_DE),
        ),
    ]

    ratings = [
        Rating(event_id=events[0].id, score=8),
        Rating(event_id=events[1].id, score=10),
        Rating(event_id=events[2].id, score=5),
    ]

    # CALCULATION
    scheduled_events = optimize_schedule(events, ratings)

    # CHECK RESULT
    assert {event.slug for event in scheduled_events} == {"foo", "baz"}
