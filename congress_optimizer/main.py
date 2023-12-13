"""Main entry point for the 37c3 schedule optimizer."""

from time import sleep

import typer

from congress_optimizer.io.api import load_events
from congress_optimizer.ratings import (
    enquire_and_save_ratings,
    filter_unrated_events,
    load_ratings,
)

app = typer.Typer(add_completion=False)


@app.command()
def rate() -> None:
    """Rate events that have not been rated yet."""

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
def dump() -> None:
    """Ouput all latest ratings to CSV, for bulk editing.

    This will exports the latest rating for each rated event.
    """

    print("To be implemented.")


@app.command()
def load() -> None:
    """Bulk load ratings from CSV.

    This will overwrite existing ratings.

    CSV format: <event_id>,<score> (e.g. 123e4567-e89b-12d3-a456-426614174000,8.5)
    Additional column will be ignored.
    """

    print("To be implemented.")


if __name__ == "__main__":
    app()
