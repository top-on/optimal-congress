"""Tests for the ratings module."""

from datetime import datetime
from uuid import uuid4

import pytest
from pytz import timezone

from optimal_congress.models import Event, EventRating, Rating
from optimal_congress.ratings import filter_latest_ratings, join_events_with_ratings

UUID1 = uuid4()
TZ_DE = timezone("Europe/Berlin")


@pytest.mark.parametrize(
    "ratings, latest_ratings",
    [
        # empty input -> empty output
        (set(), set()),
        # only one rating -> returns that rating
        (
            {Rating(event_id=UUID1, score=8, timestamp=datetime(2023, 1, 1))},
            {Rating(event_id=UUID1, score=8, timestamp=datetime(2023, 1, 1))},
        ),
        # two ratings for same event -> returns latest rating
        (
            {
                Rating(event_id=UUID1, score=8, timestamp=datetime(2023, 1, 1)),
                Rating(event_id=UUID1, score=10, timestamp=datetime(2023, 1, 2)),
            },
            {Rating(event_id=UUID1, score=10, timestamp=datetime(2023, 1, 2))},
        ),
    ],
)
def test_filter_latest_ratings(
    ratings: set[Rating], latest_ratings: set[Rating]
) -> None:
    """Test latest_ratings."""
    assert filter_latest_ratings(ratings) == latest_ratings


EVENT1 = Event(
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
EVENT2 = Event(
    id=uuid4(),
    name="bar",
    slug="bar",
    track="bar",
    assembly="bar",
    room=None,
    description="bar",
    schedule_start=datetime(2023, 12, 27, 12, tzinfo=TZ_DE),
    schedule_end=datetime(2023, 12, 27, 14, tzinfo=TZ_DE),
)
RATING1 = Rating(event_id=EVENT1.id, score=8, timestamp=datetime(2023, 1, 1))
RATING2 = Rating(event_id=EVENT1.id, score=8, timestamp=datetime(2023, 1, 1))
RATING3 = Rating(event_id=EVENT2.id, score=8, timestamp=datetime(2023, 1, 1))


@pytest.mark.parametrize(
    "ratings, events, expected",
    [
        # empty input -> empty output
        (set(), set(), set()),
        # empty ratings -> empty output
        (
            set(),
            {EVENT1},
            set(),
        ),
        # empty events -> empty output
        (
            {RATING1},
            set(),
            set(),
        ),
        # one rating, one event -> one eventrating
        (
            {RATING1},
            {EVENT1},
            {EventRating(event=EVENT1, rating=RATING1)},
        ),
        # two ratings, one event -> two eventrating
        (
            {RATING1, RATING2},
            {EVENT1},
            {
                EventRating(event=EVENT1, rating=RATING1),
                EventRating(event=EVENT1, rating=RATING2),
            },
        ),
        # two ratings, two events -> multiple eventrating
        (
            {RATING1, RATING2, RATING3},
            {EVENT1, EVENT2},
            {
                EventRating(event=EVENT1, rating=RATING1),
                EventRating(event=EVENT1, rating=RATING2),
                EventRating(event=EVENT2, rating=RATING3),
            },
        ),
    ],
)
def test_join_events_with_ratings(
    ratings: set[Rating],
    events: set[Event],
    expected: set[EventRating],
) -> None:
    """Test join_events_with_ratings."""
    result = join_events_with_ratings(ratings, events)
    assert result == expected
