from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Integrate frontend with backend
def customer(request):
    return render(request, 'restaurant_customer/restaurant_customer.html')