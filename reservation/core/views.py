from django.shortcuts import render

def index(request):
    """
    Render the reservation index page.
    """
    return render(request, "reservation/reservation.html")