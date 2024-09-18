from django.urls import path
from . import views
from .views import *

urlpatterns = [
    #path("", views.index, name="index"),
    path("", HomeView.as_view(), name="my_home_view"),
]