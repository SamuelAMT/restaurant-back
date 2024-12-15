from django.shortcuts import render

def homepage_view(request):
    return render(request, 'bookabite/main.html')

def err_404_view(request, exception):
    return render(request, 'bookabite/404.html', status=404)