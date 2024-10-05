from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from AtlantaFoodFinder.models import Locations
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Ensure this is unique
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Ensure this is unique
        blank=True,
        verbose_name='user permissions',
    )

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Locations, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    place_id = models.CharField(max_length=255, default="Unknown Place ID")
    address = models.CharField(max_length=255, default="Unknown Address")
    website = models.URLField(blank=True, null=True)
    rating = models.FloatField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    cuisine_type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=255, default="Unknown Place ID")
    rating = models.FloatField(null=True, blank=True)
    review_text = models.TextField()
    restaurant = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True, blank=True)  # Make it nullable

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name if self.restaurant else 'No Restaurant'}"
