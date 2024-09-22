from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the AtlantaFoodFinder index.")

class SignUpView():
    template_name = "users/signup.html"

#def maps(request):
 #   return redirect("CS2340/templates/maps.html")

class MapsView():
    template_name = "CS2340/maps.html"