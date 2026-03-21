from django.shortcuts import render
from django.http import JsonResponse
from .view_dependencies.gemini import verify_loc
from .view_dependencies.import_requests import get_top_places

# Create your views here.

def get_itinerary(request):
    
    return JsonResponse("place holder")