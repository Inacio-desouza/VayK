import logging
from dataclasses import dataclass, field
from typing import Optional
from django.conf import settings
import serpapi

logger = logging.getLogger(__name__)


@dataclass
class EventResult:
    ''' Normalized event shape shared across services. '''
    title: str
    date: str
    venue: str
    location: str
    source: str  # "serpapi" or "ticketmaster"
    url: Optional[str] = None
    description: Optional[str] = None

''' SerpApiService is responsible for fetching events from SerpAPI and normalizing them into our EventResult format '''
class SerpApiService:
    SOURCE = "serpapi"

    def __init__(self):
        self.client = serpapi.Client(api_key=settings.SERPAPI_KEY)

    ''' Fetch events based on destination and arrival date, returning a list of normalized EventResult objects '''
    def fetch_events(
        self,
        destination: str,   # from user input
        # event_type: str,    we could add this if we want to tighten scope here or can just let LLM handle it
        arrival_date: str,          # "MM-DD-YYYY" arrival date from user input
        engine: str = "google_events", # SerpAPI's event search parameter for the request
    ) -> list[EventResult]:         # A list of objects defined by the dataclass above!!
        
        query = f"Events in {destination} on {arrival_date}"  # We can adjust this format if needed
        try:
            raw_results = self.client.search({  # This is just the parameter format SerpAPI asks for
                "engine": engine, 
                "q": query
            }) 
            return self._normalize(raw_results)
        except Exception as exc:
            logger.error("SerpAPI fetch failed: %s", exc)
            return []          # fail gracefully so aggregator can still merge

    ''' Method to convert SerpAPI's raw response into our normalized EventResult format '''
    def _normalize(self, raw_results: dict) -> list[EventResult]:
        events = raw_results.get("events_results", [])
        normalized = []
        for event in events:
            address_parts = event.get("address", [])
            location = ", ".join(address_parts)  # "Night Club 101, 101 Avenue A, New York, NY"

            venue = event.get("venue", {})
            date = event.get("date", {})

            normalized.append(EventResult(
                title=event.get("title", ""),
                date=date.get("when") or date.get("start_date", ""),
                venue=venue.get("name", ""),
                location=location,
                url=event.get("link"),
                description=event.get("description"),
                source=self.SOURCE
            ))
        return normalized