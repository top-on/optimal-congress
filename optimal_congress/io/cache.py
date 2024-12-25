"""IO operations on local cache."""

import json

from optimal_congress.config import (
    DIR_EVENTS_CACHE,
    DIR_RATINGS_CACHE,
    DIR_ROOMS_CACHE,
)
from optimal_congress.schema import Event, Rating, Room


def save_events(
    events: set[Event],
    clear: bool = True,
) -> None:
    """Save events to cache.

    Args:
        events: List of events to save.
        clear: Whether to clear all cached events before saving. Defaults to True.
    """
    # create events cache directory, if it does not exist
    DIR_EVENTS_CACHE.mkdir(parents=True, exist_ok=True)

    # empty cache
    if clear:
        for file in DIR_EVENTS_CACHE.glob("*.json"):
            file.unlink()

    # save events
    for event in events:
        with open(DIR_EVENTS_CACHE / f"event_{event.id}.json", "w") as f:
            f.write(event.model_dump_json())


def save_rooms(
    rooms: set[Room],
    clear: bool = True,
) -> None:
    """Save rooms to cache.

    Args:s
        rooms: List of rooms to save.
        clear: Whether to clear all cached rooms before saving. Defaults to True.
    """
    # create rooms directory if it doesn't exist
    DIR_ROOMS_CACHE.mkdir(parents=True, exist_ok=True)

    # empty cache
    if clear:
        for file in DIR_ROOMS_CACHE.glob("*.json"):
            file.unlink()

    # save rooms
    for room in rooms:
        with open(DIR_ROOMS_CACHE / f"room_{room.id}.json", "w") as f:
            f.write(room.model_dump_json())


def save_rating(rating: Rating) -> None:
    """Save single new rating to cache.

    Note: This does not overwrite cached rating for the same event.
    """
    # create ratings directory if it doesn't exist
    DIR_RATINGS_CACHE.mkdir(parents=True, exist_ok=True)

    # save ratings
    with open(
        DIR_RATINGS_CACHE / f"rating_{rating.event_id}_{rating.timestamp}.json",
        "w",
    ) as f:
        f.write(rating.model_dump_json())


def load_events(exit_if_empty: bool) -> set[Event]:
    """Load events from disk.

    Args:
        exit_if_empty: Exit if no events are found, and give instructions.
    Returns:
        List of events.
    """
    # create events directory if it doesn't exist
    DIR_EVENTS_CACHE.mkdir(parents=True, exist_ok=True)

    # load events
    events_files = list(DIR_EVENTS_CACHE.glob("*.json"))
    events = {Event(**json.loads(open(file).read())) for file in events_files}

    # exit if no events are found
    if exit_if_empty and len(events) == 0:
        print("\nNo events found! Run `fetch` command to load events from API.")
        exit()
    return events


def load_rooms(exit_if_empty: bool) -> set[Room]:
    """Load rooms from disk.

    Args:
        exit_if_empty: Exit if no events are found, and give instructions.
    Returns:
        List of rooms.
    """
    # create rooms directory if it doesn't exist
    DIR_ROOMS_CACHE.mkdir(parents=True, exist_ok=True)

    # load rooms
    rooms_files = list(DIR_ROOMS_CACHE.glob("*.json"))
    rooms = {Room(**json.loads(open(file).read())) for file in rooms_files}

    # exit if no events are found
    if exit_if_empty and len(rooms) == 0:
        print("\nNo rooms found! Run `fetch` command to load room info from API.")
        exit()
    return rooms


def load_ratings(exit_if_empty: bool) -> set[Rating]:
    """Load all ratings from disk.

    Args:
        exit_if_empty: Exit if no ratings are found, and give instructions.
    Returns:
        List of ratings.
    """
    # create ratings directory if it doesn't exist
    DIR_RATINGS_CACHE.mkdir(parents=True, exist_ok=True)

    # load ratings
    ratings_files = list(DIR_RATINGS_CACHE.glob("*.json"))
    ratings = {Rating(**json.loads(open(file).read())) for file in ratings_files}

    # exit if no events are found
    if exit_if_empty and len(ratings) == 0:
        print("\nNo ratings found! Run `rate` command to rate events.")
        exit()
    return ratings
