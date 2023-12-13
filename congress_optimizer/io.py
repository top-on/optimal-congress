"""Functions for IO operations."""

import json

import requests

from congress_optimizer.config import API_EVENTS, API_ROOMS
from congress_optimizer.models import Event, Room


def load_events() -> list[Event]:
    """Load events from the API."""
    events = json.loads(s=requests.get(url=API_EVENTS).text)
    return [Event(**event) for event in events]


def load_rooms() -> list[Room]:
    """Load rooms from the API."""
    rooms = json.loads(s=requests.get(url=API_ROOMS).text)
    return [Room(**room) for room in rooms]
