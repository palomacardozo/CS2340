from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the AtlantaFoodFinder index.")

class SignUpView():
    template_name = "users/signup.html"
