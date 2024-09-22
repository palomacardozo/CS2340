from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            referer = request.META.get('HTTP_REFERER',
                                       'admin')  # Replace 'default_view_name' with a fallback URL
            return redirect(referer + "AtlantaFoodFinder/")
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})