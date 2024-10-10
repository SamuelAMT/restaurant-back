from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .models import Account

# User Registration
def create_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if Account.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        user = Account.objects.create_user(email=email, password=password)
        return JsonResponse({'message': 'User created successfully'}, status=201)

def setup_password(request, token):
    if request.method == 'POST':
        password = request.POST['password']
        uid = force_text(urlsafe_base64_decode(token))
        try:
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            return JsonResponse({'message': 'Password set successfully'}, status=200)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=400)

# Login
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Adjust as per your app structure
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

def logout_view(request):
    auth_logout(request)
    return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'auth/password_reset.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'

def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Password updated successfully'}, status=200)
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'auth/change_password.html', {'form': form})
