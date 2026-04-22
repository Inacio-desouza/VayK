from datetime import date
import logging
import time
from typing import Optional
from django.conf import settings
from .data_utils import parse_serpapi_date
import serpapi
from .event_class import EventResult  # reuse the shared dataclass

logger = logging.getLogger(__name__)

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
    ) -> list[EventResult]:         # A list of objects defined by the dataclass above!!!
        
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

    ''' Method to convert SerpAPI's raw response into our normalized format '''
    def _normalize(self, raw_results: dict) -> list[dict]:
        events = raw_results.get("events_results", [])
        normalized = []
        for event in events:
            address_parts = event.get("address", [])
            location = ", ".join(address_parts)  # "Night Club 101, 101 Avenue A, New York, NY"

            venue = event.get("venue", {})
            date_info = event.get("date", {})
            raw_date = date_info.get("start_date", "") or date_info.get("when", "")

            normalized.append({
                "title": event.get("title", ""),
                "date": raw_date,
                "venue": venue.get("name", ""),
                "location": location,
                "source": self.SOURCE,
                "url": event.get("link"),
                "description": event.get("description"),
            })
        return normalized
    
    def serp_thread(self, itinerary_view, destination, arrival_date):
        """
        Fetch events and add them to the ItineraryView in a thread-safe manner.

        Args:
            itinerary_view (ItineraryView): The ItineraryView instance to populate with events.
            destination (str): The city or location to search for events.
            arrival_date (str): Arrival date in "MM-DD-YYYY" format.

        Returns:
            None: This function modifies `itinerary_view.events` in place.
        """
        start = time.perf_counter()
        serpapi_events = self.fetch_events(destination, arrival_date)
        itinerary_view.ev_cond.acquire()
        itinerary_view.events.extend(serpapi_events)
        itinerary_view.ev_cond.notify()  # Notify that events have been added
        itinerary_view.ev_cond.release()
        elapsed = time.perf_counter() - start
        print(f"SerpAPI thread completed in {elapsed:.2f} seconds")