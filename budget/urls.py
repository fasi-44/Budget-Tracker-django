from django.urls import path, include, reverse
from django.http import HttpResponse
from django.shortcuts import redirect

def root_view(request):
    """
    Redirects the user to the login view.
    """
    return redirect(reverse('login'))  # 'login' is the name given in api/urls.py

urlpatterns = [
    path("", root_view),
    path("api/", include("api.urls")),
]