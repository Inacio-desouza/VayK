import logging
from typing import Optional
import requests
from dataclasses import dataclass
from django.conf import settings
from data_utils import parse_ticketmaster_date
from .event_class import EventResult  # reuse the shared dataclass

logger = logging.getLogger(__name__)


class TicketmasterService:
    SOURCE = "ticketmaster"
    BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

    def __init__(self):
        self.api_key = settings.TICKETMASTER_KEY

    ''' Fetch events based on destination and arrival date, returning a list of normalized EventResult objects '''
    def fetch_events(
        self,
        destination: str,   # from user input
        arrival_date: str,  # "MM-DD-YYYY" arrival date from user input
    ) -> list[EventResult]:
        # Ticketmaster expects ISO 8601: "YYYY-MM-DDT00:00:00Z"
        try:
            month, day, year = arrival_date.split("-")
            date_str = f"{year}-{month}-{day}T00:00:00Z"
        except ValueError:
            logger.error("Invalid arrival_date format: %s (expected MM-DD-YYYY)", arrival_date)
            return []

        params = {
            "apikey": self.api_key,
            "keyword": destination,
            "city": destination,
            "startDateTime": date_str,
            "endDateTime": date_str.replace("T00:00:00Z", "T23:59:59Z"),
            "size": 20,  # max results per page; bump if needed
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return self._normalize(response.json())
        except Exception as exc:
            logger.error("Ticketmaster fetch failed: %s", exc)
            return []  # fail gracefully so aggregator can still merge

    ''' Method to convert Ticketmaster's raw response into our normalized EventResult format '''
    def _normalize(self, raw_results: dict) -> list[EventResult]:
        embedded = raw_results.get("_embedded", {})
        events = embedded.get("events", [])
        normalized = []

        for event in events:
            # Venue info is nested under _embedded.venues[0]
            venues = event.get("_embedded", {}).get("venues", [])
            venue_obj = venues[0] if venues else {}
            venue_name = venue_obj.get("name", "")

            # Build a location string similar to SerpAPI's "address" join
            city = venue_obj.get("city", {}).get("name", "")
            state = venue_obj.get("state", {}).get("stateCode", "")
            address = venue_obj.get("address", {}).get("line1", "")
            location_parts = [p for p in [address, city, state] if p]
            location = ", ".join(location_parts)
            url = event.get("url")

            # Prefer localDate; fall back to the first sale date
            dates = event.get("dates", {})
            start = dates.get("start", {})
            local_date = start.get("localDate", "")      # "2026-04-24"
            local_time = start.get("localTime", "")      # "19:30:00" or missing entirely
            # Combine if both are present, otherwise fall back to just the date
            if local_date and local_time:
                raw_date = f"{local_date}T{local_time}"  # "2026-04-24T19:30:00"
            elif local_date:
                raw_date = local_date                    # "2026-04-24" — no time on record
            else:
                raw_date = start.get("dateTime", "")     # last resort: use UTC datetime


            normalized.append(EventResult(
                title=event.get("name", ""), 
                date=raw_date,
                start_dt=parse_ticketmaster_date(raw_date),
                venue=venue_name,
                location=location,
                url=url,
                description=event.get("info") or event.get("pleaseNote"),
                source=self.SOURCE,
            ))

        return normalized