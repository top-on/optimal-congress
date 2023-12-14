"""Test optimization functions."""

from datetime import datetime
from uuid import uuid4

from pytz import timezone

from optimal_congress.models import Event, Rating
from optimal_congress.optimize import optimize_schedule

TZ_DE = timezone("Europe/Berlin")

UUID1 = uuid4()
UUID2 = uuid4()
UUID3 = uuid4()


def test_optimize_schedule() -> None:
    # INPUT
    # event 'bar' overlaps with both other events
    event_ratings: list[tuple[Event, Rating]] = [
        (
            Event(
                id=UUID1,
                name="foo",
                slug="foo",
                track="foo",
                assembly="foo",
                room=None,
                description="foo",
                schedule_start=datetime(2023, 12, 27, 7, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 9, tzinfo=TZ_DE),
            ),
            Rating(event_id=UUID1, score=8),
        ),
        (
            Event(
                id=UUID2,
                name="bar",
                slug="bar",
                track="bar",
                assembly="bar",
                room=None,
                description="bar",
                schedule_start=datetime(2023, 12, 27, 8, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 10, tzinfo=TZ_DE),
            ),
            Rating(event_id=UUID2, score=10),
        ),
        (
            Event(
                id=UUID3,
                name="baz",
                slug="baz",
                track="baz",
                assembly="baz",
                room=None,
                description="baz",
                schedule_start=datetime(2023, 12, 27, 9, tzinfo=TZ_DE),
                schedule_end=datetime(2023, 12, 27, 12, tzinfo=TZ_DE),
            ),
            Rating(event_id=UUID3, score=5),
        ),
    ]

    # CALCULATION
    scheduled_events = optimize_schedule(event_ratings)

    # CHECK RESULT
    assert {event.slug for event in scheduled_events} == {"foo", "baz"}
