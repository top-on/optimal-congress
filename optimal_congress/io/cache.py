"""IO operations on local cache."""


import json

from optimal_congress.config import (
    DIR_EVENTS_CACHE,
    DIR_RATINGS_CACHE,
    DIR_ROOMS_CACHE,
)
from optimal_congress.models import Event, Rating, Room


def save_events(events: list[Event]) -> None:
    """Save events to cache.

    Note: This function overwrites all cached events.
    """
    # create events directory if it doesn't exist
    DIR_EVENTS_CACHE.mkdir(parents=True, exist_ok=True)

    # empty cache
    for file in DIR_EVENTS_CACHE.glob("*.json"):
        file.unlink()

    # save events
    for event in events:
        with open(DIR_EVENTS_CACHE / f"event_{event.id}.json", "w") as f:
            f.write(event.model_dump_json())


def save_rooms(rooms: list[Room]) -> None:
    """Save rooms to cache.

    Note: This function overwrites all cached rooms.
    """
    # create rooms directory if it doesn't exist
    DIR_ROOMS_CACHE.mkdir(parents=True, exist_ok=True)

    # empty cache
    for file in DIR_ROOMS_CACHE.glob("*.json"):
        file.unlink()

    # save rooms
    for room in rooms:
        with open(DIR_ROOMS_CACHE / f"room_{room.id}.json", "w") as f:
            f.write(room.model_dump_json())


def save_rating(rating: Rating) -> None:
    """Save an individual rating to cache.

    Note: This does not replace cached rating for the same event.
    """
    # create ratings directory if it doesn't exist
    DIR_RATINGS_CACHE.mkdir(parents=True, exist_ok=True)

    # save ratings
    with open(
        DIR_RATINGS_CACHE / f"rating_{rating.event_id}_{rating.timestamp}.json",
        "w",
    ) as f:
        f.write(rating.model_dump_json())


def load_events() -> list[Event]:
    """Load events from disk.

    Returns:
        List of events.
    """
    # create events directory if it doesn't exist
    DIR_EVENTS_CACHE.mkdir(parents=True, exist_ok=True)

    # load events
    events_files = list(DIR_EVENTS_CACHE.glob("*.json"))
    events = [Event(**json.loads(open(file).read())) for file in events_files]
    return events


def load_rooms() -> list[Room]:
    """Load rooms from disk.

    Returns:
        List of rooms.
    """
    # create rooms directory if it doesn't exist
    DIR_ROOMS_CACHE.mkdir(parents=True, exist_ok=True)

    # load rooms
    rooms_files = list(DIR_ROOMS_CACHE.glob("*.json"))
    rooms = [Room(**json.loads(open(file).read())) for file in rooms_files]
    return rooms


def load_ratings() -> list[Rating]:
    """Load all ratings from disk.

    Returns:
        List of ratings.
    """
    # create ratings directory if it doesn't exist
    DIR_RATINGS_CACHE.mkdir(parents=True, exist_ok=True)

    # load ratings
    ratings_files = list(DIR_RATINGS_CACHE.glob("*.json"))
    ratings = [Rating(**json.loads(open(file).read())) for file in ratings_files]
    return ratings
