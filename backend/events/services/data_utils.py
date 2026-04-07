from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def parse_serpapi_date(raw: str) -> Optional[datetime]:
    '''
    SerpAPI returns strings like:
      "Fri, Apr 25, 8 - 11 PM"     <- has start time
      "Fri, Apr 25"                 <- date only
    We extract the start time and ignore the end.
    '''
    if not raw:
        return None

    # Strip the end time range if present: "8 – 11 PM" --> "8 PM"
    # The dash separates start and end; keep only the left side + the trailing AM/PM
    if "-" in raw:
        parts = raw.split("-")
        # parts[0]: "Fri, Apr 25, 8 "   parts[1]: " 11 PM"
        period = parts[1].strip().split()[-1]           # "PM" or "AM"
        raw = parts[0].strip() + " " + period           # "Fri, Apr 25, 8 PM"

    current_year = datetime.now().year
    raw_with_year = f"{raw} {current_year}"

    for fmt in (
        "%a, %b %d, %I %p %Y",     # "Fri, Apr 25, 8 PM 2026"
        "%a, %b %d %Y",             # "Fri, Apr 25 2026"  (date-only fallback)
    ):
        try:
            return datetime.strptime(raw_with_year, fmt)
        except ValueError:
            continue

    logger.warning("Could not parse SerpAPI date: %r", raw)
    return None


def parse_ticketmaster_date(raw: str) -> Optional[datetime]:
    '''
    Ticketmaster returns strings like:
      "2026-04-24T19:30:00"    <- datetime
      "2026-04-24"             <- date only (no time on record)
    '''
    if not raw:
        return None

    for fmt in (
        "%Y-%m-%dT%H:%M:%S",    # with time
        "%Y-%m-%dT%H:%M:%SZ",   # with UTC Z suffix
        "%Y-%m-%d",              # date only
    ):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue

    logger.warning("Could not parse Ticketmaster date: %r", raw)
    return None