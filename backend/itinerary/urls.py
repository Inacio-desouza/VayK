from django.urls import path
from . import views

urlpatterns = [
    path('get_itinerary/', views.get_itinerary)
]