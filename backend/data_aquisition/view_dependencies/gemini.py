from google import genai
from google.genai import types
from django.conf import settings
import json

API_KEY = settings.GEMINI_KEY
if not API_KEY:
    raise ValueError("API_KEY is not set")

# 1. Setup Client with your AI Studio API Key
# Get your key at: https://aistudio.google.com/app/apikey
client = genai.Client(api_key=API_KEY)

def generate_itinerary(activities, events, interests, preferences, arrival, departure):
    model_id = "gemini-3.1-pro"

    config = types.GenerateContentConfig(
    system_instruction="""
    You are a travel itinerary generator.

    You will receive:
    - arrival date/time
    - departure date/time
    - user interests
    - user preferences
    - a list of activities
    - a list of events

    Your task is to generate a travel itinerary within the arrival and departure range.

    Rules:
    1. ONLY use the activities and events provided. Do not invent new items.
    2. The itinerary must occur between the arrival and departure times.
    3. Events must be scheduled on their provided date/time.
    4. Activities may be scheduled at any reasonable time within the date range.
    5. Select items that best match the user's interests and preferences.
    6. Do not duplicate the same event or activity.
    7. Mix activities and events when possible to create a balanced itinerary.
    8. The itinerary must be sorted chronologically by date_time.

    Field rules:

    For activities:
    - name = activity name
    - date_time = generated time within trip window
    - address = activity address
    - description = null
    - rating = activity rating
    - reviews = activity num_reviews
    - url = null

    For events:
    - name = event title
    - date_time = event date
    - address = venue or location
    - description = event description
    - rating = null
    - reviews = null
    - url = event url

    Return ONLY a JSON object. Do not include explanations or extra text.
    """,

        temperature=0.3,
        response_mime_type="application/json",

        response_schema={
            "type": "OBJECT",
            "properties": {
                "itinerary": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "name": {"type": "STRING"},
                            "date_time": {"type": "STRING"},
                            "address": {"type": "STRING"},
                            "description": {"type": ["STRING", "NULL"]},
                            "rating": {"type": ["NUMBER", "NULL"]},
                            "reviews": {"type": ["NUMBER", "NULL"]},
                            "url": {"type": ["STRING", "NULL"]}
                        },
                        "required": [
                            "name",
                            "date_time",
                            "address",
                            "description",
                            "rating",
                            "reviews",
                            "url"
                        ]
                    }
                }
            },
            "required": ["itinerary"]
        }
    )

    response = client.models.generate_content(
        model=model_id,
        contents={
            "arrival": arrival,
            "departure": departure,
            "interests": interests,
            "preferences": preferences,
            "activities": activities,
            "events": events
        },
        config=config
    )

    return json.loads(response.text)
