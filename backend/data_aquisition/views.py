from django.shortcuts import render
from django.http import JsonResponse
from .view_dependencies.gemini import generate_itinerary
from .view_dependencies.import_requests import get_top_places
from .models import City, Activity
import json

# Create your views here.

def get_itinerary(request):
    if request.method == "POST":
        data = json.loads(request.body)

        lat = data.get("lat")
        lon = data.get("lon")
        destination = data.get("destination")
        arrival_date = data.get("arrivalDate")
        departure_date = data.get("departureDate")
        interests = data.get("interests")
        preferences = data.get("preferences")

        city_object = City.objects.filter(name=destination, latitude=lat, longitude=lon).exists()
        if not city_object:
            city_object = City.objects.get_or_create(
                name=destination,
                defaults={
                    "latitude": lat,
                    "longitude": lon,
                }
            )
            activities = get_top_places(lat, lon)
            for activity in activities:
                Activity.objects.create(
                    city=city_object,
                    name=activity["name"],
                    icon=activity["icon"],
                    rating=activity["rating"],
                    num_reviews=activity["reviews"],
                    score=activity["score"],
                    address=activity["address"]
                )

        activities = list(Activity.objects.filter(city=city_object).values())
        events = []  # Placeholder for events data, can be populated similarly to activities
        itinerary = generate_itinerary(activities, events, interests, preferences, arrival_date, departure_date)
            

        # Example response
        return JsonResponse({
            "itinerary": itinerary["itinerary"]
            "alternates": itinerary["alternates"]
        })

    return JsonResponse({"error": "POST request required"}, status=400)
