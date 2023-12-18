"""Main entry point for the 37c3 schedule optimizer."""
# %%
import logging
from pathlib import Path

import pandas as pd
import typer
from typing_extensions import Annotated

from optimal_congress.io.api import fetch_events, fetch_rooms
from optimal_congress.io.cache import (
    load_events,
    load_ratings,
    save_events,
    save_ratings,
    save_rooms,
)
from optimal_congress.models import Rating, RatingsExport
from optimal_congress.optimize import optimize_schedule
from optimal_congress.ratings import (
    enquire_and_save_ratings,
    filter_latest_ratings,
    filter_unrated_events,
    join_events_with_ratings,
)

app = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


# %%
@app.callback()
def users_callback(verbose: bool = typer.Option(False, "-v", "--verbose")) -> None:
    """Optimize your personal schedule for the 37c3."""
    # set log level
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s")


@app.command()
def fetch(
    dry: bool = typer.Option(
        default=False, help="At dryrun, local cache is not changed."
    ),
) -> None:
    """Fetch events and rooms from API, and update local cache."""

    # fetch from API
    print("Fetching events and rooms from API...")
    events_api = fetch_events()
    rooms_api = fetch_rooms()

    # print summary
    print(f"Fetched {len(events_api)} events and {len(rooms_api)} rooms from API.")

    print("\nComparing API with cache...")
    events_cache = load_events(exit_if_empty=False)

    # check for changes
    new_events = events_api - events_cache
    removed_events = events_cache - events_api
    # report changes
    print(
        f"Found {len(new_events)} new events, and {len(removed_events)} removed events."
    )
    if new_events:
        print("\nNew events:")
        for event in new_events:
            print(f"- {event.name[:50]:.<52}{event.url}")
    if removed_events:
        print("\nRemoved events:")
        for event in removed_events:
            print(f"- {event.name[:50]:.<52}{event.url}")

    # save to cache, if not dryrun
    if dry:
        print("\nDryrun, not updating cache.")
        exit()
    print("\nUpdating cache...")
    save_events(events_api)
    save_rooms(rooms_api)
    print("Done.")


@app.command()
def rate() -> None:
    """Interactively rate those events that have not been rated yet."""

    print("loading events and ratings from cache...")
    events = load_events(exit_if_empty=True)
    ratings = load_ratings(exit_if_empty=False)

    print(f"\nFound {len(events)} events and {len(ratings)} ratings.")

    unrated_events = filter_unrated_events(
        events=events,
        ratings=ratings,
    )
    if len(unrated_events) == 0:
        print("\nNo new events to rate. Exiting.")
        exit()

    enquire_and_save_ratings(events=unrated_events)
    print("Done.")


@app.command()
def ratings() -> None:
    """List all latest ratings."""

    print("loading events and ratings from cache...")
    events = load_events(exit_if_empty=True)
    ratings = load_ratings(exit_if_empty=True)

    # latest ratings with their events
    latest_ratings = filter_latest_ratings(ratings)
    event_ratings = join_events_with_ratings(
        ratings=latest_ratings,
        events=events,
    )

    # print descenting ratings
    event_ratings_sorted = sorted(
        list(event_ratings),
        key=lambda x: x.rating.score,
        reverse=True,
    )
    print("\nLatest ratings:")
    for event_rating in event_ratings_sorted:
        print(
            f"- Rating: {event_rating.rating.score} "
            f"- {event_rating.event.name[:50]:.<52}{event_rating.event.url}"
        )


@app.command()
def optimize(
    minimum_rating: float = typer.Option(
        0.0,
        "-m",
        "--min",
        help="Minimum rating required for talk to be considered in optimization.",
    ),
) -> None:
    """Optimize the schedule based on ratings."""

    print("loading events and ratings from cache...")
    ratings = load_ratings(exit_if_empty=True)
    events = load_events(exit_if_empty=True)

    # latest ratings with their events
    latest_ratings = filter_latest_ratings(ratings)
    event_ratings = join_events_with_ratings(
        ratings=latest_ratings,
        events=events,
    )

    # filter events by minimum required rating
    event_ratings_filtered = {
        event_rating
        for event_rating in event_ratings
        if event_rating.rating.score >= minimum_rating
    }

    # optimize schedule
    scheduled_events = optimize_schedule(event_ratings=event_ratings_filtered)

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
def dump(
    file_path: Annotated[
        str,
        typer.Argument(
            help="Relative or absolute path to which CSV file will be exported.",
        ),
    ],
) -> None:
    """Export all latest ratings to CSV, for bulk editing.

    This will exports the latest rating for each rated event.
    """
    # convert argument to absolute path
    path = Path(file_path)
    absolute_path = path if path.is_absolute() else Path.cwd() / path

    # load events and ratings
    print("loading events and ratings from cache...")
    events = load_events(exit_if_empty=True)
    ratings = load_ratings(exit_if_empty=True)

    # latest ratings with their events
    latest_ratings = filter_latest_ratings(ratings)
    event_ratings = join_events_with_ratings(
        ratings=latest_ratings,
        events=events,
    )

    # export to CSV
    print(f"Exporting {len(event_ratings)} ratings to {absolute_path}...")
    ratings_df = RatingsExport(
        pd.DataFrame(
            data=[
                [
                    event_rating.rating.score,
                    event_rating.event.name,
                    event_rating.event.url,
                    event_rating.event.id,
                ]
                for event_rating in event_ratings
            ],
            columns=["rating", "name", "url", "event_id"],
        ).sort_values(by="rating", ascending=False)
    )

    ratings_df.to_csv(path_or_buf=absolute_path, index=False)
    print("Done.")


@app.command()
def load(
    file_path: Annotated[
        str,
        typer.Argument(
            help="Name and relative or absolute path from which to read in CSV.",
        ),
    ],
    dry: bool = typer.Option(
        default=False, help="At dryrun, local cache is not changed."
    ),
) -> None:
    """Bulk import ratings from CSV.

    This will overwrite existing ratings.

    CSV format should be the same one as what the `dump` command exports.
    """
    # convert argument to absolute path
    path = Path(file_path)
    absolute_path = path if path.is_absolute() else Path.cwd() / path

    # load ratings from CSV
    ratings_df = RatingsExport(
        pd.read_csv(filepath_or_buffer=absolute_path, index_col=False)
    )
    if len(ratings_df) == 0:
        print("No ratings found in CSV. Exiting.")
        exit()

    # convert to Rating objects
    ratings = {
        Rating(
            event_id=row["event_id"],
            score=row["rating"],
        )
        for _, row in ratings_df.iterrows()
    }

    # save ratings
    if dry:
        print("\nDryrun, not updating cache.")
        exit()
    print(f"Saving {len(ratings)} ratings to cache...")
    save_ratings(ratings=ratings)


# %%
if __name__ == "__main__":
    app()
