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

MIN_REVIEWS = 500

SCORE_THRESHOLD = 60

URL = "https://places.googleapis.com/v1/places:searchNearby"

MILES_TO_METERS = 1609.34

PLACE_TYPES = [
    ["tourist_attraction"],
    ["bar", "restaurant", "cultural_landmark"]
]

# =====================================
# SCORE FUNCTION
# =====================================

def compute_score(rating, reviews):

    if rating == 0 or reviews == 0:
        return 0

    return (rating ** 2) * math.log10(reviews)


# =====================================
# GRID + RADIUS CALCULATION
# =====================================

def compute_cell_radius():

    spacing = (2 * SEARCH_RADIUS_MILES) / (GRID_SIZE - 1)

    radius_miles = spacing / math.sqrt(2)

    return int(radius_miles * MILES_TO_METERS)


def build_grid(CENTER_LAT, CENTER_LNG):

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



def make_request_with_retry(url, body, headers, max_retries=5):
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
            return []

        results = data.get("places", [])

        for p in results:
            p["place_type"] = place_type

        places.extend(results)

    return places


# =====================================
# PLACE COLLECTION
# =====================================

def collect_places(LAT, LNG):

    all_places = {}

    grid = build_grid(LAT, LNG)

    cell_radius = compute_cell_radius()

    for lat, lng in grid:

        results = fetch_places(lat, lng, cell_radius)

        print(f"Fetched {len(results)} places for cell centered at ({lat}, {lng})")

        for p in results:

            place_id = p.get("id")

            if place_id in all_places:
                continue

            ptype = p.get("place_type")
            rating = p.get("rating", 0)
            reviews = p.get("userRatingCount", 0)
            score = compute_score(rating, reviews)

            if ptype == "restaurant" and score < 10 + SCORE_THRESHOLD:
                continue

            if ptype == "bar" and score < 10 + SCORE_THRESHOLD:
                continue

            if ptype == "tourist_attraction" and score < SCORE_THRESHOLD:
                continue

            if ptype == "cultural_landmark" and score < SCORE_THRESHOLD - 10:
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

    return list(all_places.values())


# =====================================
# RANKING
# =====================================

def get_top_places(LAT, LNG):

    places = collect_places(LAT, LNG)

    print(f"Collected {len(places)} places")

    sorted_places = sorted(
        places,
        key=lambda x: x["score"],
        reverse=True
    )

    return sorted_places


#fix database attributes
def thread_top_places(city_object, lat, lng):
    activities = get_top_places(lat, lng)
    for activity in activities:
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
    return


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    results = get_top_places(40.0194, -105.2527)

    print("\nTop Tourist Attractions:\n")

    for p in results:

        print(
            f'{p["score"]:.2f} | '
            f'{p["rating"]}⭐ '
            f'({p["reviews"]} reviews) | '
            f'{p["name"]} | '
            f'{p["address"]}'
        )