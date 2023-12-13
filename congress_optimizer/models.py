"""Model definitions."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from congress_optimizer.config import HUB_EVENT_ROUTE


class Room(BaseModel):
    """A room."""

    id: UUID
    name: str
    assembly: str


class Event(BaseModel):
    """An event."""

    id: UUID
    name: str
    slug: str
    track: str | None
    assembly: str
    room: UUID | None
    description: str
    schedule_start: datetime
    schedule_end: datetime

    def __str__(self) -> str:
        """Return a string representation of the event."""
        # get time without timezone
        local_time = self.schedule_start.strftime("%Y-%m-%d %H:%M")
        return f"'{self.name}' ({local_time}, {self.url})"

    @property
    def url(self) -> str:
        """Return the url of the event."""
        return f"{HUB_EVENT_ROUTE}/{self.slug}"
