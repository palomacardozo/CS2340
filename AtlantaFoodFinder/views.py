from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def HomeView(request):
    return render(request, 'users/base.html', {})

class SignUpView():
    template_name = "users/signup.html"

#def maps(request):
#   return redirect("CS2340/templates/maps.html")

class MapsView():
    template_name = "CS2340/maps.html"

class PasswordResetView():
    template_name = "users/passwordresetform.html"

class PasswordResetDoneView():
    template_name = "users/passwordresetdone.html"

class PasswordResetConfirmedView():
    template_name = "users/passwordresetconfirmed.html"

class PasswordResetCompleteView():
    template_name = "users/passwordresetcomplete.html"