"""Integration tests for API functions."""

from optimal_congress.io.api import fetch_events


def test_fetch_events():
    """Test fetching events from the API."""
    fetch_events()
