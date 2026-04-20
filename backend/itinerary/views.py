from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .view_dependencies.gemini import generate_itinerary
from .view_dependencies.places import thread_top_places
from .view_dependencies.ticketmaster import TicketmasterService
from .view_dependencies.serp import SerpApiService
from .models import City, Activity
import threading
import json
import time
from threading import Condition

# Create your views here.
class ItineraryView:
    def __init__(self):
        self.activities_short = []
        self.activities_full = []
        self.events = []
        self.ev_cond = Condition()

def thread_activities(city_object, itinerary_view):
    itinerary_view.activities_full = list(Activity.objects.filter(city=city_object).values())
    for activity in itinerary_view.activities_full:
        itinerary_view.activities_short.append({
            "name": activity["name"],
            "rating": activity["rating"],
            "reviews": activity["num_reviews"],
        })
    return

@csrf_exempt
def get_itinerary(request):
    
    if request.method == "POST":
        data = json.loads(request.body)

        start_time = time.perf_counter()

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
            places_thread = threading.Thread(target=thread_top_places, args=(city_object, lat, lon))
            places_thread.start()
        
        print("Getting from events")
        serpapi = SerpApiService()
        ticketmaster = TicketmasterService()
        serp_thread = threading.Thread(target=serpapi.serp_thread, args=(itinerary_view, destination, arrival_date))
        serp_thread.start()
        ticketmaster_thread = threading.Thread(target=ticketmaster.ticketmaster_thread, args=(itinerary_view, destination, arrival_date, departure_date))
        ticketmaster_thread.start()

        if places_thread:
            places_thread.join()  # Wait for the places thread to finish before generating the itinerary
            print("Finished getting from google places")
        
        print("Getting from database")
        activities_thread = threading.Thread(target=thread_activities, args=(city_object, itinerary_view))
        activities_thread.start()

        #join for the event thread here
        serp_thread.join()  # Wait for the SerpAPI thread to finish before generating the itinerary
        ticketmaster_thread.join()  # Wait for the Ticketmaster thread to finish before generating the itinerary
        activities_thread.join()  # Wait for the activities thread to finish before generating the itinerary
        print("Finished getting from database and events")

        print("Generating itinerary with Gemini")
        itinerary = generate_itinerary(itinerary_view.activities_full, itinerary_view.activities_short, itinerary_view.events, interests, preferences, arrival_date, departure_date)
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Total time for itinerary generation: {elapsed_time:.2f} seconds")

        # Example response
        return JsonResponse({
            "itinerary": itinerary["itinerary"],
            "alternates": itinerary["alternates"]
        })

    return JsonResponse({"error": "POST request required"}, status=400)
