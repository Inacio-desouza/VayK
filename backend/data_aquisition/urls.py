from django.urls import path
from . import views

urlpatterns = [
    path('itinerary/', views.get_itinerary)
]