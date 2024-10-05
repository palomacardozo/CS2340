from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
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

    for fav in user_favorites:
        print(fav.restaurant.name, fav.restaurant.address)

    return render(request, 'users/favorites.html', {'favorites': user_favorites})

@login_required(login_url='/login/')
def add_to_favorites(request, place_id):
    # Get the location using place_id
    #location = get_object_or_404(Locations, place_id=place_id)

    # Handle AJAX request
    # Diff types of requests: for example, googling is a get request.
    # POST takes data from the user- "posting data"
    # JSON- js format with key value pairs
    # What I want each url to do with each data request- what data is being posted to me

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
            rating=place['result'].get('rating', None),  # Get rating from place details
            phone_number=place['result'].get('formatted_phone_number', None),  # Get phone number
            cuisine_type=', '.join(place['result'].get('types', [])),  # Join types as a string for cuisine
            website=place['result'].get('website', None),
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
def remove_favorite(request, pk):
    Favorite.objects.get(pk=pk).delete()
    return redirect('/favorites')

def add_to_favorites(request, restaurant_id):
    restaurant = get_object_or_404(Locations, id=restaurant_id)
    Favorite.objects.create(user=request.user, restaurant=restaurant)
    return redirect('favorites')  # Redirect to the favorites page


@login_required(login_url='/login/')
def submit_review(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id = data.get('restaurant')
            rating = data.get('rating')
            review_text = data.get('review')

            print(f"Received data: {data}")  # Log received data for debugging

            restaurant = Restaurant.objects.get(id=restaurant_id)

            # Check if the user has already submitted a review for this restaurant
            existing_review = Review.objects.filter(user=request.user, restaurant=restaurant).first()

            if existing_review:
                # Update the existing review
                existing_review.rating = rating
                existing_review.review_text = review_text
                existing_review.save()
                message = 'Review updated successfully!'
            else:
                # Create a new review
                new_review = Review(
                    user=request.user,
                    restaurant=restaurant,
                    rating=rating,
                    review_text=review_text,
                )
                new_review.save()
                message = 'Review submitted successfully!'

            return JsonResponse({'message': message}, status=201)
        except Exception as e:
            print(f"Error while submitting review: {e}")  # Log the error for debugging
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required
def my_reviews(request):
    user_reviews = Review.objects.filter(user=request.user)  # Fetch reviews created by the logged-in user
    return render(request, 'users/my_reviews.html', {'reviews': user_reviews})

@login_required(login_url='/login/')
def remove_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('/my_reviews')