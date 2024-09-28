"""
URL configuration for CS2340 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("SignUp/", views.signup, name="signup"),
    path('login/', views.login_view, name='login'),
    path("", include("AtlantaFoodFinder.urls")),
    path("", views.base, name='home'),
    path('login/', views.login_view, name='login'),

    path('passwordreset/', views.PasswordResetView, name='passwordreset'),
    path('passwordreset/done/', views.PasswordResetDoneView, name='passwordresetdone'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmedView, name='passwordresetconfirm'),
    path('reset/done/', views.PasswordResetCompleteView, name='passwordresetcomplete'),
]
