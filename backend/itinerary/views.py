from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .view_dependencies.gemini import generate_itinerary
from .view_dependencies.places import thread_top_places
from .models import City, Activity
import threading
import json

# Create your views here.
class ItineraryView:
    def __init__(self):
        self.activities = []
        self.events = []

def thread_activities(city_object, itinerary_view):
    itinerary_view.activities = list(Activity.objects.filter(city=city_object).values())
    return

@csrf_exempt
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
        itinerary_view = ItineraryView()

        city_object, created = City.objects.get_or_create(name=destination,
                                                    defaults={
                                                        "latitude": lat,
                                                        "longitude": lon,
                                                    }
                                                )
        places_thread = None
        if created:
            print("Getting from google places")
            places_thread = threading.Thread(target=thread_top_places, args=(lat, lon))
            places_thread.start()
        
        print("Getting from events")
        events_thread = None  # Placeholder for events data, can be populated similarly to activities

        if places_thread:
            places_thread.join()  # Wait for the places thread to finish before generating the itinerary
            print("Finished getting from google places")
        
        print("Getting from database")
        activities_thread = threading.Thread(target=thread_activities, args=(city_object, itinerary_view))
        activities_thread.start()

        #join for the event thead here
        activities_thread.join()  # Wait for the activities thread to finish before generating the itinerary
        print("Finished getting from database and events")

        itinerary = generate_itinerary(itinerary_view.activities, itinerary_view.events, interests, preferences, arrival_date, departure_date)
            

        # Example response
        return JsonResponse({
            "itinerary": itinerary["itinerary"],
            "alternates": itinerary["alternates"]
        })

    return JsonResponse({"error": "POST request required"}, status=400)
