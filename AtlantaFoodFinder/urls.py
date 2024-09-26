from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.HomeView, name="HomeView"),
    #path("", views.index, name="index"),
]