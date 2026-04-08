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
    icon = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    num_reviews = models.IntegerField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.city.name})"