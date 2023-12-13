"""Main entry point for the 37c3 schedule optimizer."""

# %%

from congress_optimizer.io import load_events, load_rooms

# %%

print("loading Events and Rooms...")
rooms = load_rooms()
events = load_events()

# %%

str(events[0])

# %%
