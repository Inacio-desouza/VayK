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
    """
    A container class for holding itinerary data during async processing.

    Attributes:
        activities_short (list[dict]): Shortened activity objects for AI prompts.
        activities_full (list[dict]): Full activity objects with all fields.
        events (list[dict]): Event objects fetched from external APIs.
        ev_cond (Condition): Threading condition for event synchronization.
    """
    def __init__(self):
        self.activities_short = []
        self.activities_full = []
        self.activities_success = True
        self.events = []
        self.ev_cond = Condition()

def thread_activities(city_object, itinerary_view):
    """
    Populate the ItineraryView with activities from the database.

    Runs in a separate thread to fetch activities for a given city and
    build both full and short representations.

    Args:
        city_object: A City model instance to filter activities.
        itinerary_view (ItineraryView): The ItineraryView instance to populate
            with activities_short and activities_full.

    Returns:
        None: This function modifies `itinerary_view` in place.
    """
    start = time.perf_counter()
    itinerary_view.activities_full = list(Activity.objects.filter(city=city_object).values())
    for activity in itinerary_view.activities_full:
        itinerary_view.activities_short.append({
            "name": activity["name"],
            "rating": activity["rating"],
            "reviews": activity["num_reviews"],
            "address": activity["address"]
        })
    elapsed = time.perf_counter() - start
    print(f"Activities thread completed in {elapsed:.2f} seconds")
    return

@csrf_exempt
def get_itinerary(request):
    """
    Generate a travel itinerary based on user input.

    Accepts a POST request with destination, dates, interests, and preferences.
    Orchestrates parallel fetching from Google Places, SerpAPI, and Ticketmaster,
    then uses Gemini AI to generate an itinerary and alternates.

    Args:
        request (HttpRequest): The Django HTTP request object. Must be a POST
            with JSON body containing: lat, lon, destination, arrivalDate,
            departureDate, interests, and preferences.

    Returns:
        JsonResponse: A JSON response with "itinerary" and "alternates" keys.
            Returns an error response with status 400 if not a POST request.

    Expected POST body:
        {
            "lat": float,
            "lon": float,
            "destination": str,
            "arrivalDate": str,
            "departureDate": str,
            "interests": list[str],
            "preferences": str
        }
    """
    
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
        activities_thread = None
        if created:
            print("Getting from google places")
            places_thread = threading.Thread(target=thread_top_places, args=(itinerary_view, city_object, lat, lon))
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
        
        else:
            print("Getting from database")
            activities_thread = threading.Thread(target=thread_activities, args=(city_object, itinerary_view))
            activities_thread.start()

        #join for the event thread here
        serp_thread.join()  # Wait for the SerpAPI thread to finish before generating the itinerary
        ticketmaster_thread.join()  # Wait for the Ticketmaster thread to finish before generating the itinerary
        if activities_thread:
            activities_thread.join()  # Wait for the activities thread to finish before generating the itinerary
        print("Finished getting from database and events")

        print("Generating itinerary with Gemini")
        itinerary = generate_itinerary(itinerary_view.activities_full, itinerary_view.activities_short, itinerary_view.events, interests, preferences, arrival_date, departure_date)

        if itinerary_view.activities_success == False:
            City.objects.filter(id=city_object.id).delete()

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Total time for itinerary generation: {elapsed_time:.2f} seconds")

        # Example response
        return JsonResponse({
            "itinerary": itinerary["itinerary"],
            "alternates": itinerary["alternates"]
        })

    return JsonResponse({"error": "POST request required"}, status=400)
