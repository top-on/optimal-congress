"""Main entry point for the 37c3 schedule optimizer."""

import logging
from time import sleep

import typer

from congress_optimizer.io.api import load_events
from congress_optimizer.optimize import optimize_schedule
from congress_optimizer.ratings import (
    enquire_and_save_ratings,
    filter_latest_ratings,
    filter_unrated_events,
    load_ratings,
)

app = typer.Typer(add_completion=False)


@app.command()
def fetch() -> None:
    """Fetch events and rooms from API, and update local cache."""

    print("To be implemented.")


@app.command()
def rate() -> None:
    """Interactively rate those events that have not been rated yet."""

    print("fetching events...")
    events = load_events()

    print("loading previous ratings...")
    previous_ratings = load_ratings()

    print(f"\nFound {len(events)} events and {len(previous_ratings)} ratings.")
    sleep(1)

    unrated_events = filter_unrated_events(
        events=events,
        ratings=previous_ratings,
    )
    if len(unrated_events) == 0:
        print("\nNo new events to rate. Exiting.")
        exit()

    enquire_and_save_ratings(events=unrated_events)


@app.command()
def ratings() -> None:
    """List all latest ratings."""

    ratings = load_ratings()
    events = load_events()

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


@app.callback()
def users_callback(verbose: bool = typer.Option(False, "-v", "--verbose")) -> None:
    # set log level
    log_level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format="%(message)s")


@app.command()
def optimize() -> None:
    """Optimize the schedule based on ratings."""

    ratings = load_ratings()
    events = load_events()

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
