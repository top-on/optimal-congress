"""Main entry point for the 37c3 schedule optimizer."""

from time import sleep

from congress_optimizer.io.api import load_events
from congress_optimizer.ratings import (
    enquire_and_save_ratings,
    filter_unrated_events,
    load_ratings,
)

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
