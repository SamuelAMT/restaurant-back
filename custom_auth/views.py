from ninja import Schema
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpRequest
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from .models import Account, Session, LoginLog


class UserCreateSchema(Schema):
    email: str
    password: str


class LoginSchema(Schema):
    email: str
    password: str


class ChangePasswordSchema(Schema):
    old_password: str
    new_password: str


class PasswordResetSchema(Schema):
    password: str


class PasswordResetRequestSchema(Schema):
    email: str
    
def testing_endpoints(request):
    return render(request, 'custom_auth/testing_endpoints.html')


def create_user(request: HttpRequest, payload: UserCreateSchema):
    email = payload.email
    password = payload.password
    if Account.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)
    user = Account.objects.create_user(email=email, password=password)
    return JsonResponse({"message": "User created successfully"}, status=201)


def setup_password(request: HttpRequest, token: str, payload: PasswordResetSchema):
    password = payload.password
    uid = force_str(urlsafe_base64_decode(token))
    try:
        user = Account.objects.get(pk=uid)
        user.set_password(password)
        user.save()
        return JsonResponse({"message": "Password set successfully"}, status=200)
    except Account.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=400)


def login(request: HttpRequest, payload: LoginSchema):
    email = payload.email
    password = payload.password
    user = authenticate(username=email, password=password)
    if user is not None:
        auth_login(request, user)
        session_key = get_random_string(32)
        Session.objects.create(
            account=user, session_key=session_key, ip_address="127.0.0.1"
        )
        LoginLog.objects.create(account=user, ip_address="127.0.0.1", action="login")
        return JsonResponse({"message": "Login successful"}, status=200)
    return JsonResponse({"error": "Invalid credentials"}, status=400)


def logout(request: HttpRequest):
    auth_logout(request)
    LoginLog.objects.create(account=None, ip_address="127.0.0.1", action="logout")
    return JsonResponse({"message": "Logged out successfully"}, status=200)


def request_password_reset(request: HttpRequest, payload: PasswordResetRequestSchema):
    email = payload.email
    try:
        user = Account.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        send_mail(
            "Password Reset Request",
            f"Please use the following link to reset your password: {reset_url}",
            "support@yourdomain.com",
            [email],
            fail_silently=False,
        )
        return JsonResponse({"message": "Password reset email sent"}, status=200)
    except Account.DoesNotExist:
        return JsonResponse({"error": "Email not found"}, status=404)


def reset_password(
    request: HttpRequest, uidb64: str, token: str, payload: PasswordResetSchema
):
    password = payload.password
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            LoginLog.objects.create(account=user, action="password_reset")
            return JsonResponse({"message": "Password reset successful"}, status=200)
        return JsonResponse({"error": "Invalid token"}, status=400)
    except Account.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)


def change_password(request: HttpRequest, payload: ChangePasswordSchema):
    old_password = payload.old_password
    new_password = payload.new_password
    user = authenticate(username="current_email", password=old_password)
    if user is not None:
        user.set_password(new_password)
        user.save()
        return JsonResponse({"message": "Password changed successfully"}, status=200)
    return JsonResponse({"error": "Invalid credentials"}, status=400)


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
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