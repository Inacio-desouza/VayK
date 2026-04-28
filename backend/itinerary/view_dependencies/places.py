import random

import requests
import time
import math
import numpy as np
from django.conf import settings
from itinerary.models import City, Activity

# =====================================
# CONFIGURATION
# =====================================

API_KEY = settings.PLACES_KEY
if not API_KEY:
    raise ValueError("API_KEY is not set")

SEARCH_RADIUS_MILES = 20
GRID_SIZE = 2

MIN_REVIEWS = 1000

SCORE_THRESHOLD = 50

URL = "https://places.googleapis.com/v1/places:searchNearby"

MILES_TO_METERS = 1609.34

PLACE_TYPES = [
    ["tourist_attraction", "cultural_landmark", "wildlife_park"],
    ["bar", "restaurant", "night_club"]
]

# =====================================
# SCORE FUNCTION
# =====================================

def compute_score(rating, reviews):
    """
    Compute a relevance score for a place based on its rating and number of reviews.

    Args:
        rating (float): The place's rating (e.g., 4.5).
        reviews (int): The number of reviews for the place.

    Returns:
        float: The computed score. Returns 0 if rating or reviews is 0.
    """

    if rating == 0 or reviews == 0:
        return 0

    return (rating ** 2) * math.log10(reviews)


# =====================================
# GRID + RADIUS CALCULATION
# =====================================

def compute_cell_radius():
    """
    Calculate the radius for each grid cell in meters.

    The radius is based on the search radius and grid size, ensuring
    cells cover the entire search area without overlap.

    Returns:
        int: The radius in meters for each grid cell.
    """

    spacing = (2 * SEARCH_RADIUS_MILES) / (GRID_SIZE - 1)

    radius_miles = spacing / math.sqrt(2)

    return int(radius_miles * MILES_TO_METERS)


def build_grid(CENTER_LAT, CENTER_LNG):
    """
    Build a grid of coordinate points around a center location.

    Creates a grid of lat/lng points within the search radius, sorted
    by distance from the center (closest first).

    Args:
        CENTER_LAT (float): The latitude of the center point.
        CENTER_LNG (float): The longitude of the center point.

    Returns:
        list[tuple[float, float]]: A list of (latitude, longitude) tuples
            sorted by distance from the center.
    """

    miles_per_degree = 69

    lat_offset = SEARCH_RADIUS_MILES / miles_per_degree

    lng_offset = SEARCH_RADIUS_MILES / (
        miles_per_degree * math.cos(math.radians(CENTER_LAT))
    )

    lat_points = np.linspace(
        CENTER_LAT - lat_offset,
        CENTER_LAT + lat_offset,
        GRID_SIZE
    )

    lng_points = np.linspace(
        CENTER_LNG - lng_offset,
        CENTER_LNG + lng_offset,
        GRID_SIZE
    )

    grid = []

    for lat in lat_points:
        for lng in lng_points:

            dist = math.sqrt(
                (lat - CENTER_LAT) ** 2 +
                (lng - CENTER_LNG) ** 2
            )

            grid.append((dist, lat, lng))

    grid.sort(key=lambda x: x[0])

    return [(lat, lng) for _, lat, lng in grid]



def make_request_with_retry(url, body, headers, max_retries=3):
    """
    Make an HTTP POST request with exponential backoff retry logic.

    Args:
        url (str): The URL to send the POST request to.
        body (dict): The JSON body for the request.
        headers (dict): The HTTP headers for the request.
        max_retries (int, optional): Maximum number of retry attempts. Defaults to 5.

    Returns:
        dict or None: The JSON response data if successful, or None if all retries fail.
    """
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=body, headers=headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            print("RESPONSE:", response.text)

            # If last attempt, give up
            if attempt == max_retries - 1:
                return None

            # Exponential backoff with jitter
            sleep_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(sleep_time)


# =====================================
# GOOGLE PLACES REQUEST
# =====================================

def fetch_places(lat, lng, radius):
    """
    Fetch places from Google Places API for a given location and radius.

    Queries the Google Places API for tourist attractions, cultural landmarks,
    wildlife parks, bars, restaurants, and night clubs within the specified radius.

    Args:
        lat (float): The latitude of the search center.
        lng (float): The longitude of the search center.
        radius (int): The search radius in meters.

    Returns:
        list[dict]: A list of place dictionaries with details including ID,
            display name, address, rating, reviews, types, and editorial summary.
            Returns an empty list if the request fails.
    """
    places = []

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": ",".join([
            "places.id",
            "places.regularOpeningHours",
            "places.displayName",
            "places.formattedAddress",
            "places.location",
            "places.rating",
            "places.userRatingCount",
            "places.googleMapsUri",
            "places.types",
            "places.editorialSummary"
        ])
    }

    for place_type in PLACE_TYPES:

        body = {
            "includedTypes": place_type,
            "maxResultCount": 20,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lng
                    },
                    "radius": radius
                }
            },
            "rankPreference": "POPULARITY"
        }

        data = make_request_with_retry(URL, body, headers)

        if not data:
            return None

        results = data.get("places", [])

        for p in results:
            p["place_type"] = place_type

        places.extend(results)

    return places


# =====================================
# PLACE COLLECTION
# =====================================

def collect_places(LAT, LNG):
    """
    Collect and filter places from Google Places API across a grid of locations.

    Builds a grid around the center coordinates, fetches places from each cell,
    applies score-based filtering, and deduplicates results.

    Args:
        LAT (float): The latitude of the search center.
        LNG (float): The longitude of the search center.

    Returns:
        list[dict]: A list of place dictionaries containing name, hours,
            address, description, rating, reviews, URL, score, latitude, and longitude.
    """

    all_places = {}

    grid = build_grid(LAT, LNG)

    cell_radius = compute_cell_radius()

    success = True

    for lat, lng in grid:

        results = fetch_places(lat, lng, cell_radius)

        if results is None:
            print("Failed to fetch places for cell centered at "
                  f"({lat}, {lng}). Skipping this cell.")
            success = False
            continue

        print(f"Fetched {len(results)} places for cell centered at ({lat}, {lng})")

        for p in results:

            place_id = p.get("id")

            if place_id in all_places:
                continue

            ptype = p.get("place_type")
            rating = p.get("rating", 0)
            reviews = p.get("userRatingCount", 0)
            score = compute_score(rating, reviews)

            if reviews < MIN_REVIEWS:
                if rating < 4.0:
                    continue

            else: 
                if score < SCORE_THRESHOLD:
                    continue

            name = p.get("displayName", {}).get("text")
            address = p.get("formattedAddress")
            location = p.get("location", {})
            hours = p.get("regularOpeningHours", {}).get("periods", [])
            lat = location.get("latitude")
            lng = location.get("longitude")
            url = p.get("googleMapsUri")
            description = p.get("editorialSummary", {}).get("text")

            all_places[place_id] = {
                "name": name,
                "date_time": hours,
                "address": address,
                "description": description,
                "rating": rating,
                "reviews": reviews,
                "url": url,
                "score": score,
                "lat": lat,
                "lng": lng
            }

    return {'places': list(all_places.values()), 'success': success}


# =====================================
# RANKING
# =====================================

def get_top_places(LAT, LNG):
    """
    Get the top-rated places for a given location, sorted by score.

    Collects all places within the search radius and returns them sorted
    by relevance score in descending order.

    Args:
        LAT (float): The latitude of the search center.
        LNG (float): The longitude of the search center.

    Returns:
        list[dict]: A list of place dictionaries sorted by score (highest first).
    """

    results = collect_places(LAT, LNG)

    print(f"Collected {len(results['places'])} places")

    sorted_places = sorted(
        results['places'],
        key=lambda x: x["score"],
        reverse=True
    )

    return {'places': sorted_places, 'success': results['success']}


#fix database attributes
def thread_top_places(itinerary_view, city_object, lat, lng):
    """
    Fetch top places and save them as Activity objects in the database.

    Retrieves the top places for the given coordinates and creates
    Activity records associated with the provided city object.

    Args:
        itinerary_view (ItineraryView): The ItineraryView instance to populate
            with activities_short and activities_full.
        city_object: A City model instance to associate with the activities.
        lat (float): The latitude of the search center.
        lng (float): The longitude of the search center.

    Returns:
        None: This function does not return a value. Activities are
            persisted to the database via the Activity model.
    """
    start = time.perf_counter()
    result = get_top_places(lat, lng)

    if result['success'] == False:
        print("No places found for the given location.")
        itinerary_view.activities_success = False

    for activity in result['places']:
                Activity.objects.create(
                    city=city_object,
                    name=activity["name"],
                    rating=activity["rating"],
                    num_reviews=activity["reviews"],
                    score=activity["score"],
                    address=activity["address"],
                    latitude=activity["lat"],
                    longitude=activity["lng"],
                    description=activity["description"],
                    url=activity["url"],
                    date_time=activity["date_time"]
                )
                itinerary_view.activities_full.append({
                    "name": activity["name"],
                    "rating": activity["rating"],
                    "reviews": activity["reviews"],
                    "address": activity["address"],
                    "description": activity["description"],
                    "url": activity["url"],
                    "date_time": activity["date_time"]
                })
                itinerary_view.activities_short.append({
                    "name": activity["name"],
                    "rating": activity["rating"],
                    "reviews": activity["reviews"],
                    "address": activity["address"]
                })
    elapsed = time.perf_counter() - start
    print(f"Places thread completed in {elapsed:.2f} seconds")
    return


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    results = get_top_places(40.0194, -105.2527)

    print("\nTop Tourist Attractions:\n")

    for p in results['places']:

        print(
            f'{p["score"]:.2f} | '
            f'{p["rating"]}⭐ '
            f'({p["reviews"]} reviews) | '
            f'{p["name"]} | '
            f'{p["address"]}'
        )