from google import genai
from google.genai import types
from django.conf import settings

API_KEY = settings.GEMINI_KEY
if not API_KEY:
    raise ValueError("API_KEY is not set")

# 1. Setup Client with your AI Studio API Key
# Get your key at: https://aistudio.google.com/app/apikey
client = genai.Client(api_key=API_KEY)

def verify_loc(city, country):
    model_id = "gemini-3.1-flash-lite-preview"

    config = types.GenerateContentConfig(
        system_instruction="""Verify if a provided location is real.
        Return a JSON dictionary with keys "real", "lat", and "log".
        1. 'real': 'y' if it's a physical Earth location, 'n' otherwise.
        2. 'lat' and 'log': Float coordinates of the center (null if not real).
        Return ONLY the JSON object.""",
        temperature=0.1,
        response_mime_type="application/json",
        # This enforces the structure at the model level
        response_schema={
            "type": "OBJECT",
            "properties": {
                "real": {"type": "STRING", "enum": ["y", "n"]},
                "lat": {"type": "NUMBER"},
                "log": {"type": "NUMBER"}
            },
            "required": ["real", "lat", "log"]
        }
    )

    response = client.models.generate_content(
        model=model_id,
        contents="{city}, {country}",
        config=config
    )

    return response.text