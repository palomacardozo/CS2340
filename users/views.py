from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.shortcuts import get_object_or_404
from AtlantaFoodFinder.models import Locations
import googlemaps
from django.conf import settings
import json
from django.contrib.auth import get_user_model
from users.models import Favorite

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

    for fav in user_favorites:
        print(fav.restaurant.name, fav.restaurant.address)

    return render(request, 'users/favorites.html', {'favorites': user_favorites})

@login_required(login_url='/login/')
def add_to_favorites(request, place_id):
    # Get the location using place_id
    #location = get_object_or_404(Locations, place_id=place_id)

    # Handle AJAX request
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)

        print(data)

        is_favorited = data.get('favorited')

        print(f"is_favorited: {is_favorited}")

        place = get_place_details(place_id)

        # Check if the location already exists in the Locations model
        location, location_created = Locations.objects.get_or_create(
            place_id=place_id,
            defaults={
                'name': place['result']['name'],
                'address': place['result']['formatted_address'],
                'lat': place['result']['geometry']['location']['lat'],
                'lng': place['result']['geometry']['location']['lng'],
            }
        )

        favorite, favorite_created = Favorite.objects.get_or_create(
            user=request.user, # Saved for each user
            place_id=place_id,
            restaurant=location,
            address=place['result']['formatted_address'],
            website=place['result'].get('website', None)
        )
        if not favorite_created or not is_favorited:
            print(f"Restaurant with place_id {place_id} else from favorites.")
            Favorite.objects.filter(user=request.user, place_id=place_id).delete()
        else:
            print(f"Restaurant {place['result']['name']} saved to favorites!")

        return JsonResponse({'status': 'success'})

    # Handle non-AJAX requests
    return JsonResponse({'status': 'error'}, status=400)

@login_required(login_url='/login/')
def remove_favorite(request, place_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            Favorite.objects.filter(user=request.user, place_id=place_id).delete()
            return JsonResponse({'status': 'success'})
        except Favorite.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)
