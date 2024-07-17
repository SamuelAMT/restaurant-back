from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Integrate frontend with backend
def index(request):
    return render(request, 'reservation/index.html')