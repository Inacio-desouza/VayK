from google import genai
from google.genai import types
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import json
import time

API_KEY = settings.GEMINI_KEY
if not API_KEY:
    raise ValueError("API_KEY is not set")

client = genai.Client(api_key=API_KEY)

# Reconstruct the full objects from the indices
def map_item(item, activities, events, is_itinerary):
    """
    Reconstruct a full activity/event object from a compact reference.

    Converts a lightweight reference (containing 'source' and 'index') into
    a full object with all available fields. Differentiates between activities
    and events since they have different field names.

    Args:
        item (dict): A dictionary containing 'source' ('activity' or 'event')
            and 'index' (position in the source list). If `is_itinerary` is True,
            also contains 'recommended_time'.
        activities (list[dict]): Full list of activity objects.
        events (list[dict]): Full list of event objects.
        is_itinerary (bool): If True, uses 'recommended_time' from the item;
            if False, returns None for 'recommended_time'.

    Returns:
        dict: A reconstructed object with keys: name, date_time, address,
            description, rating, reviews, url, and recommended_time.
    """
    source_list = activities if item['source'] == 'activity' else events
    original = source_list[item['index']]
    res = {}
    if item['source'] == 'activity':
        res["name"] = original.get('name')
        res["date_time"] = original.get('date_time')
        res["address"] = original.get('address')
        res["description"] = original.get('description')
        res["rating"] = original.get('rating')
        res["reviews"] = original.get('reviews')
        res["url"] = original.get('url')

    else:
        res["name"] = original.get('title')
        res["date_time"] = original.get('date')
        res["address"] = original.get('venue')
        res["description"] = original.get('description')
        res["rating"] = None  # Events may not have ratings
        res["reviews"] = None  # Events may not have reviews
        res["url"] = original.get('url')

    if is_itinerary:
        res["recommended_time"] = item['recommended_time']
    else:
        res["recommended_time"] = None

    return res

def generate_itinerary(act_full, act_short, events, interests, preferences, arrival, departure):
    """
    Generate a travel itinerary using Gemini AI based on user preferences.

    Sends activities and events to Gemini with user interests and date range.
    Returns a structured itinerary and alternate recommendations.

    Args:
        act_full (list[dict]): Full activity objects with all fields.
        act_short (list[dict]): Shortened activity objects for the prompt.
        events (list[dict]): List of event objects.
        interests (list[str]): User's travel interests (e.g., ['food', 'art']).
        preferences (str): User's preferences as a string description.
        arrival (str): Arrival date string (e.g., '2024-06-01').
        departure (str): Departure date string (e.g., '2024-06-07').

    Returns:
        dict: A dictionary with two keys:
            - "itinerary" (list[dict]): Selected activities/events with recommended times.
            - "alternates" (list[dict]): 10 alternative recommendations without times.

    Raises:
        ValueError: If the response exceeds max tokens.
    """
    model_id = 'gemini-3.1-flash-lite-preview'

    start_time = time.perf_counter()

    config = types.GenerateContentConfig(
        system_instruction="""
        You are a travel expert. You will receive two lists: 'activities' and 'events'.
        Your goal is to select the best items based on their relevance to the user's interests and preferences.
        
        Scheduling Rules:
        1. Itinerary Density: Provide exactly 2 to 3 items for every full day of the trip.
        2. Proximity Logic: Group items scheduled on the same day by geographic proximity. Look at the 'address' fields to ensure activities for a single day are in the same neighborhood or within a reasonable transit distance.
        3. Logical Flow: Order items within a day chronologically (e.g., Morning, Afternoon, Evening).
        
        Prioritization Rules:
        1. Prioritize local activities and unique local events.
        2. Strictly avoid large national brand names or global chains.
        
        Output Rules:
        - Itinerary: Return an array of objects. Each object must have an 'index' (the original position in the provided list), a 'source' ('activity' or 'event'), and a 'recommended_time'.
        - Alternates: Return exactly 10 'index' and 'source' pairs for items not in the itinerary.
        """,
        temperature=0.1,
        response_mime_type="application/json",
        response_schema={
            "type": "OBJECT",
            "properties": {
                "itinerary": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "index": {"type": "INTEGER"},
                            "source": {"type": "STRING", "enum": ["activity", "event"]},
                            "recommended_time": {"type": "STRING", "description": "Format: YYYY-MM-DD HH:MM AM/PM"}
                        },
                        "required": ["index", "source", "recommended_time"]
                    }
                },
                "alternates": {
                    "type": "ARRAY",
                    "minItems": 10,
                    "maxItems": 10,
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "index": {"type": "INTEGER"},
                            "source": {"type": "STRING", "enum": ["activity", "event"]}
                        },
                        "required": ["index", "source"]
                    }
                }
            },
            "required": ["itinerary", "alternates"]
        }
    )

    prompt = json.dumps({
        "arrival": arrival,
        "departure": departure,
        "interests": interests,
        "preferences": preferences,
        "activities": act_short,
        "events": events
    }, cls=DjangoJSONEncoder)

    response = client.models.generate_content(
        model=model_id,
        contents=prompt,
        config=config
    )

    if response.candidates[0].finish_reason == 'MAX_TOKENS':
    # Handle the error gracefully or retry with a higher limit
        raise ValueError("The response was too long and was cut off.")

    raw_data = json.loads(response.text)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    print(f"Itinerary generated in {elapsed_time:.2f} seconds.")

    final_itinerary = [map_item(i, act_full, events, True) for i in raw_data['itinerary']]
    final_alternates = [map_item(i, act_full, events, False) for i in raw_data['alternates']]

    return {
        "itinerary": final_itinerary,
        "alternates": final_alternates
    }
