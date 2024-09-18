from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
import googlemaps
import json
from django.conf import settings
from .models import *


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the AtlantaFoodFinder index.")

class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'mydata'
    model = Locations
    #form_class = EmailForm
    success_url = "/"