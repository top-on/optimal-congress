"""Functions for read operations against congress API."""

import json

import requests

from congress_optimizer.config import API_EVENTS, API_ROOMS
from congress_optimizer.models import Event, Room


def fetch_events() -> list[Event]:
    """Load events from the API."""
    events = json.loads(s=requests.get(url=API_EVENTS).text)
    return [Event(**event) for event in events]


def fetch_rooms() -> list[Room]:
    """Load rooms from the API."""
    rooms = json.loads(s=requests.get(url=API_ROOMS).text)
    return [Room(**room) for room in rooms]
