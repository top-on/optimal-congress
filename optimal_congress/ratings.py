"""Functions related to ratings."""

import os

from optimal_congress.config import DIR_RATINGS_CACHE
from optimal_congress.models import Event, EventRating, Rating


def filter_latest_ratings(ratings: set[Rating]) -> set[Rating]:
    """Return the latest rating for each event.

    Args:
        ratings: List of ratings.
    Returns:
        List of latest ratings.
    """
    # sort ratings by timestamp, descending
    ratings_sorted = sorted(
        list(ratings), key=lambda rating: rating.timestamp, reverse=True
    )

    # keep only latest rating for each event
    latest_ratings: set[Rating] = set()
    for rating in ratings_sorted:
        if rating.event_id not in [r.event_id for r in latest_ratings]:
            latest_ratings.add(rating)
    return latest_ratings


def filter_unrated_events(
    events: set[Event],
    ratings: set[Rating],
) -> set[Event]:
    """Return the unrated events from a list of events based on previous ratings.

    Args:
        events: list of events.
        previous_ratings: list of previous ratings.
    Returns:
        List of events for which no rating is provided.
    """
    rated_event_ids = {rating.event_id for rating in ratings}
    unrated_events = {event for event in events if event.id not in rated_event_ids}
    return unrated_events


def enquire_and_save_ratings(events: set[Event]) -> None:
    """Enquire and save ratings for a list of events."""

    for i, event in enumerate(events):
        os.system("cls" if os.name == "nt" else "clear")
        timestamp_start = event.schedule_start.strftime("%Y-%m-%d %H:%M")
        time_end = event.schedule_end.strftime("%H:%M")
        print(
            f"\nUnrated event ({i + 1}/{len(events)}):"
            f"\n\n{timestamp_start} - {time_end}"
            f"\n\n{event.name}"
            f"\n\n{event.description}"
            f"\n\n{event.url}"
        )
        try:
            score = input("\nRate from 0 to 10 (Enter to exit): ")
            if score == "":
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            print("\nExiting.")
            break

        rating = Rating(event_id=event.id, score=float(score))

        # save rating
        with open(DIR_RATINGS_CACHE / f"rating_{event.id}.json", "w") as f:
            print(f"Saving rating '{rating.score}' for event '{event.name}'...")
            f.write(rating.model_dump_json())


def join_events_with_ratings(
    ratings: set[Rating],
    events: set[Event],
) -> set[EventRating]:
    """Inner-Join events with ratings.

    Note that duplicated ratings are not removed, if they are provided as input.

    Args:
        events: Set of events.
        ratings: Set of ratings.
    Returns:
        Ratings with their associated Events.
    """
    # join events with ratings
    event_ratings: set[EventRating] = set()
    for rating in ratings:
        matching_events = {event for event in events if event.id == rating.event_id}
        if matching_events:
            event = {event for event in events if event.id == rating.event_id}.pop()
            event_ratings.add(EventRating(event=event, rating=rating))

    return event_ratings
