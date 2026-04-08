from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class EventResult:
    ''' Normalized event shape shared across services. '''
    title: str
    date: str           # raw string from source, kept for debugging
    start_dt: Optional[datetime] = None   # normalized - format: "2026-04-24T19:30:00" or "2026-04-24" if time is missing
    venue: str
    location: str
    source: str         # "serpapi" or "ticketmaster"
    url: Optional[str] = None
    description: Optional[str] = None
    