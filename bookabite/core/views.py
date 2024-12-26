from django.shortcuts import render

def homepage_view(request):
    return render(request, 'core/home.html')

def err_404_view(request, exception):
    return render(request, 'core/errors/404.html', status=404)