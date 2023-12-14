"""App configuration."""

from pathlib import Path

# URLS
API_EVENTS = "https://events.ccc.de/congress/2023/hub/api/c/37c3/events"
API_ROOMS = "https://events.ccc.de/congress/2023/hub/api/c/37c3/rooms"
HUB_EVENT_ROUTE = "https://events.ccc.de/congress/2023/hub/en/event"

# folder to store serialized ratings
DIR_RATINGS_CACHE = Path.home() / ".cache/congress_optimizer/ratings"
DIR_EVENTS_CACHE = Path.home() / ".cache/congress_optimizer/events"
DIR_ROOMS_CACHE = Path.home() / ".cache/congress_optimizer/rooms"
