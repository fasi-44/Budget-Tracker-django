from django.urls import path, include
from django.http import HttpResponse

def root_view(request):
    """
    This view will handle requests to the root URL ("/").
    You can customize this to return a simple message,
    a welcome page, or redirect to another part of your application.
    """
    return HttpResponse("Welcome to your Budget Tracker API!")  # Simplest response

urlpatterns = [
    path("", root_view),  # Add this line for the root URL
    path("api/", include("api.urls")),
]