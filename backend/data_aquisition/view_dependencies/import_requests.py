import requests
import time
import math
import numpy as np
from django.conf import settings

# =====================================
# CONFIGURATION
# =====================================

API_KEY = settings.PLACES_KEY
if not API_KEY:
    raise ValueError("API_KEY is not set")

SEARCH_RADIUS_MILES = 30
GRID_SIZE = 3

MIN_REVIEWS = 500

PAGE_SCORE_THRESHOLD = 60
MAX_PAGES = 3

URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

MILES_TO_METERS = 1609.34

PLACE_TYPES = [
    "tourist_attraction",
    "bar",
    "restaurant"
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


# =====================================
# GOOGLE PLACES REQUEST
# =====================================

def fetch_places(lat, lng, radius):

    places = []

    for place_type in PLACE_TYPES:

        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "type": place_type,
            "key": API_KEY
        }

        page_count = 0

        while True:

            response = requests.get(URL, params=params).json()

            results = response.get("results", [])

            # store the type so later filters can use it
            for r in results:
                r["place_type"] = place_type

            places.extend(results)

            page_count += 1

            scores = []

            for p in results:

                rating = p.get("rating", 0)
                reviews = p.get("user_ratings_total", 0)

                scores.append(compute_score(rating, reviews))

            avg_score = sum(scores) / max(len(scores), 1)

            token = response.get("next_page_token")

            if not token:
                break

            if avg_score < PAGE_SCORE_THRESHOLD:
                break

            if page_count >= MAX_PAGES:
                break

            time.sleep(2)

            params = {
                "pagetoken": token,
                "key": API_KEY
            }

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

        for p in results:

            reviews = p.get("user_ratings_total", 0)
            rating = p.get("rating", 0)
            ptype = p["place_type"]

            if ptype == "restaurant" and reviews < 10 * MIN_REVIEWS:
                continue

            if ptype == "bar" and reviews < 10 * MIN_REVIEWS:
                continue

            if ptype == "tourist_attraction" and reviews < MIN_REVIEWS:
                continue

            place_id = p["place_id"]

            if place_id in all_places:
                continue

            score = compute_score(rating, reviews)

            all_places[place_id] = {
                "name": p["name"],
                "icon": p["icon"],
                "rating": rating,
                "reviews": reviews,
                "score": score,
                "address": p.get("vicinity"),
                "lat": p["geometry"]["location"]["lat"],
                "lng": p["geometry"]["location"]["lng"]
            }

    return list(all_places.values())


# =====================================
# RANKING
# =====================================

def get_top_places(LAT, LNG):

    places = collect_places(LAT, LNG)

    sorted_places = sorted(
        places,
        key=lambda x: x["score"],
        reverse=True
    )

    return sorted_places


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