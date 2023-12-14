"""Tests for the ratings module."""

from datetime import datetime
from uuid import uuid4

import pytest

from congress_optimizer.models import Rating
from congress_optimizer.ratings import filter_latest_ratings

UUID1 = uuid4()


@pytest.mark.parametrize(
    "ratings, latest_ratings",
    [
        # empty input -> empty output
        ([], []),
        # only one rating -> returns that rating
        (
            [Rating(event_id=UUID1, score=8, timestamp=datetime(2023, 1, 1))],
            [Rating(event_id=UUID1, score=8, timestamp=datetime(2023, 1, 1))],
        ),
        # two ratings for same event -> returns latest rating
        (
            [
                Rating(event_id=UUID1, score=8, timestamp=datetime(2023, 1, 1)),
                Rating(event_id=UUID1, score=10, timestamp=datetime(2023, 1, 2)),
            ],
            [Rating(event_id=UUID1, score=10, timestamp=datetime(2023, 1, 2))],
        ),
    ],
)
def test_filter_latest_ratings(
    ratings: list[Rating], latest_ratings: list[Rating]
) -> None:
    """Test latest_ratings."""
    assert filter_latest_ratings(ratings) == latest_ratings
