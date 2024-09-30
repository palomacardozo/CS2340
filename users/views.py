from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.shortcuts import get_object_or_404
from AtlantaFoodFinder.models import Locations
from .models import Favorite
import googlemaps
from django.conf import settings
import json

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(base)
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "users/base.html")  # Redirect to a home page after successful login
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def base(request):
    return render(request, 'users/base.html', {})

def get_place_details(place_id):
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    place_details = gmaps.place(place_id=place_id)
    return place_details

def favorites(request):
    if not request.user.is_authenticated:
        return render(request, 'users/favorites.html', {'message': "You must log in or sign up to view favorites."})
    user_favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'users/favorites.html', {'favorites': user_favorites})

@login_required(login_url='/login/')
def add_to_favorites(request, place_id):
    # Get the location using place_id instead of restaurant_id
    location = get_object_or_404(Locations, place_id=place_id)

    # Handle AJAX request
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        is_favorited = data.get('favorited')

        if is_favorited:
            # Add to favorites
            Favorite.objects.get_or_create(user=request.user, location=location)
        else:
            # Remove from favorites
            Favorite.objects.filter(user=request.user, location=location).delete()

        return JsonResponse({'status': 'success'})

    # Handle non-AJAX requests
    return JsonResponse({'status': 'error'}, status=400)