"""App configuration."""

from pathlib import Path

# URLS
API_EVENTS = "https://events.ccc.de/congress/2023/hub/api/c/37c3/events"
API_ROOMS = "https://events.ccc.de/congress/2023/hub/api/c/37c3/rooms"
HUB_EVENT_ROUTE = "https://events.ccc.de/congress/2023/hub/en/event"

# folder to store serialized ratings
RATINGS_DIR = Path.home() / ".cache/congress_optimizer/ratings"
