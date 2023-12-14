"""Main entry point for the 37c3 schedule optimizer."""

import logging
from time import sleep

import typer

from optimal_congress.io.api import fetch_events, fetch_rooms
from optimal_congress.io.cache import (
    load_events,
    load_ratings,
    save_events,
    save_rooms,
)
from optimal_congress.optimize import optimize_schedule
from optimal_congress.ratings import (
    enquire_and_save_ratings,
    filter_latest_ratings,
    filter_unrated_events,
)

app = typer.Typer(add_completion=False)


@app.callback()
def users_callback(verbose: bool = typer.Option(False, "-v", "--verbose")) -> None:
    """Optimize your personal schedule for the 37c3."""
    # set log level
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s")


@app.command()
def fetch() -> None:
    """Fetch events and rooms from API, and update local cache."""

    # fetch from API
    print("Fetching events and rooms from API...")
    events = fetch_events()
    rooms = fetch_rooms()

    # print summary
    print(f"Found {len(events)} events and {len(rooms)} rooms at API.")

    # save to cache
    print("Saving events and rooms to cache...")
    save_events(events)
    save_rooms(rooms)


@app.command()
def rate() -> None:
    """Interactively rate those events that have not been rated yet."""

    print("loading events and ratings from cache...")
    events = load_events()
    ratings = load_ratings()
    if len(events) == 0:
        print("\nNo events found! Run `fetch` operation to load events from API.")
        exit()

    print(f"\nFound {len(events)} events and {len(ratings)} ratings.")
    sleep(1)

    unrated_events = filter_unrated_events(
        events=events,
        ratings=ratings,
    )
    if len(unrated_events) == 0:
        print("\nNo new events to rate. Exiting.")
        exit()

    enquire_and_save_ratings(events=unrated_events)


@app.command()
def ratings() -> None:
    """List all latest ratings."""

    print("loading events and ratings from cache...")
    events = load_events()
    ratings = load_ratings()
    if len(events) == 0:
        print("\nNo events found! Run `fetch` operation to load events from API.")
        exit()
    if len(ratings) == 0:
        print("\nNo ratings found! Run `rate` operation to rate events.")
        exit()

    latest_ratings = filter_latest_ratings(ratings)
    ratings_sorted = sorted(
        latest_ratings, key=lambda rating: rating.score, reverse=True
    )

    # join ratings with events
    rating_event = [
        (rating, [event for event in events if event.id == rating.event_id][0])
        for rating in ratings_sorted
    ]

    # print ratings for each event
    print("Latest ratings:")
    for rating, event in rating_event:
        print(f"- Rating: {rating.score} - {event.name[:50]:.<52}{event.url}")


@app.command()
def optimize() -> None:
    """Optimize the schedule based on ratings."""

    print("loading events and ratings from cache...")
    ratings = load_ratings()
    events = load_events()
    if len(ratings) == 0 or len(events) == 0:
        print(
            "\nNo ratings or events found! Do the following:"
            "\n1. Run `fetch` operation to load events from API."
            "\n2. Run `rate` operation to rate events."
            "\n3. Run `ratings` operation to check your ratings."
        )
        exit()

    latest_ratings = filter_latest_ratings(ratings)

    # join ratings with events
    events_ratings = [
        ([event for event in events if event.id == rating.event_id][0], rating)
        for rating in latest_ratings
    ]

    # optimize schedule
    scheduled_events = optimize_schedule(events_ratings=events_ratings)

    events_sorted = sorted(
        scheduled_events, key=lambda event: event.schedule_start, reverse=False
    )

    # print scheduled events
    print("Scheduled events:")
    for event in events_sorted:
        start_time = event.schedule_start.strftime("%a %d %H:%M")
        end_time = event.schedule_end.strftime("%H:%M")
        print(f"- {start_time}-{end_time}: {event.name[:50]:.<53}{event.url}")


@app.command()
def dump() -> None:
    """Export all latest ratings to CSV, for bulk editing.

    This will exports the latest rating for each rated event.
    """

    print("To be implemented.")


@app.command()
def load() -> None:
    """Bulk import ratings from CSV.

    This will overwrite existing ratings.

    CSV format: <event_id>,<score> (e.g. 123e4567-e89b-12d3-a456-426614174000,8.5)
    Additional column will be ignored.
    """

    print("To be implemented.")


if __name__ == "__main__":
    app()
