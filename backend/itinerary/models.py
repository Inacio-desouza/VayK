from django.utils import timezone

from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "cities"

class Activity(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="activities")

    name = models.CharField(max_length=200)

    # Core metrics
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    num_reviews = models.IntegerField(null=True, blank=True)
    score = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    # Location
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # New API fields
    description = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)

    # Store hours as JSON (flexible structure)
    date_time = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.city.name})"