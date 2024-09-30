from django.shortcuts import render, redirect
from django.http import HttpResponse

from AtlantaFoodFinder.models import Locations


# Create your views here.
def HomeView(request):
    restaurants = Locations.objects.all()  # or filter as needed
    return render(request, 'users/base.html', {'restaurants': restaurants})

class SignUpView():
    template_name = "users/signup.html"

#def maps(request):
#   return redirect("CS2340/templates/maps.html")

class MapsView():
    template_name = "CS2340/maps.html"
