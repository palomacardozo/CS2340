from django.db import models

# Create your models here.

class Locations(models.Model):
    club = models.CharField(max_length=500,blank=True, null=True)
    name = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=200,blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    country = models.CharField(max_length=200,blank=True, null=True)
    address = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)

    lat = models.CharField(max_length=200,blank=True, null=True)
    lng = models.CharField(max_length=200,blank=True, null=True)
    place_id = models.CharField(max_length=200,blank=True, null=True)
    def __str__(self):
         return self.name

class Distances(models.Model):
    from_location = models.ForeignKey(Locations, related_name='from_distances', on_delete=models.CASCADE)
    to_location = models.ForeignKey(Locations, related_name='to_distances', on_delete=models.CASCADE)
    mode = models.CharField(max_length=20, choices=[
        ("driving", "Driving"),
        ("walking", "Walking"),
        ("bicycling", "Bicycling"),
        ("transit", "Transit")
        ])
    distance_km = models.FloatField()
    duration_mins = models.IntegerField()
    duration_traffic_mins = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Distance from {self.from_location} to {self.to_location} ({self.mode})"