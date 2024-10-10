from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.conf import settings
from .models import Account, Session, LoginLog

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
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            # Register the session
            session_key = request.session.session_key or get_random_string(32)
            Session.objects.create(account=user, session_key=session_key, ip_address=request.META.get('REMOTE_ADDR'))
            # Log the login action
            LoginLog.objects.create(account=user, ip_address=request.META.get('REMOTE_ADDR'), user_agent=request.META.get('HTTP_USER_AGENT'), action='login')
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

# Logout
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        # Log the logout action
        LoginLog.objects.create(account=request.user, ip_address=request.META.get('REMOTE_ADDR'), user_agent=request.META.get('HTTP_USER_AGENT'), action='logout')
        return JsonResponse({'message': 'Logged out successfully'}, status=200)
    return JsonResponse({'error': 'Not authenticated'}, status=400)

# Password Reset Request
def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = Account.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            send_mail(
                'Password Reset Request',
                f'Please use the following link to reset your password: {reset_url}',
                'support@yourdomain.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Password reset email sent'}, status=200)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Email not found'}, status=404)

# Password Reset Form (POST only)
def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                # Log password reset action
                LoginLog.objects.create(account=user, ip_address=request.META.get('REMOTE_ADDR'), user_agent=request.META.get('HTTP_USER_AGENT'), action='password_reset')
                return JsonResponse({'message': 'Password reset successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid token'}, status=400)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
