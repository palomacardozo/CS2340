from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.shortcuts import get_object_or_404
from AtlantaFoodFinder.models import Locations
from .models import Favorite
import googlemaps
from django.conf import settings
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Review

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
def add_to_favorites(request, restaurant_id):
    restaurant = get_object_or_404(Locations, id=restaurant_id)
    Favorite.objects.create(user=request.user, restaurant=restaurant)
    return redirect('favorites')  # Redirect to the favorites page


@csrf_exempt  # Temporarily disable CSRF for testing (remove after testing)
@login_required(login_url='/login/')
def submit_review(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Extract relevant data
            restaurant_id = data.get('restaurant')  # Ensure this matches your frontend
            rating = data.get('rating')
            review_text = data.get('review')

            # Debugging output
            print(f'Restaurant ID: {restaurant_id}, Rating: {rating}, Review: {review_text}')

            # Create and save the review
            new_review = Review(
                restaurant_id=restaurant_id,  # stored internally as restaurant_id
                # user=request.user,  # if we wanted to associate the review with the logged-in user
                rating=rating,
                review_text=review_text
            )
            new_review.save()

            return JsonResponse({'message': 'Review submitted successfully!'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)



