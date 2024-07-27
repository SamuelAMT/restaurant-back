from django.contrib.auth import login as auth_login, authenticate, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from .forms import RegisterForm, LoginForm

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'message': 'Successfully logged in'}, status=200)
            return JsonResponse({'message': 'Invalid credentials'}, status=401)
        return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Successfully logged out'}, status=200)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def csrf(request):
    if request.method == 'GET':
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token}, status=200)
    return JsonResponse({'message': 'Invalid request method'}, status=405)