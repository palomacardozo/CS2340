from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from AtlantaFoodFinder.views import index
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(index)
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})