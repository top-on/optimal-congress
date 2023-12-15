"""Functions for read operations against congress API."""

import json

import requests

from optimal_congress.config import API_EVENTS, API_ROOMS
from optimal_congress.models import Event, Room


def fetch_events() -> set[Event]:
    """Load events from the API."""
    events_dict = json.loads(s=requests.get(url=API_EVENTS).text)
    events = {Event(**event) for event in events_dict}
    if len(events) == 0:
        raise ValueError("No events found! Check state of congress API.")
    return events


def fetch_rooms() -> set[Room]:
    """Load rooms from the API."""
    rooms_dict = json.loads(s=requests.get(url=API_ROOMS).text)
    rooms = {Room(**room) for room in rooms_dict}
    if len(rooms) == 0:
        raise ValueError("No rooms found! Check state of congress API.")
    return rooms
