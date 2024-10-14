from ninja import Schema, Request
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .models import Account, Session, LoginLog
from django.contrib.auth.tokens import default_token_generator


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


def create_user(request: Request, payload: UserCreateSchema):
    email = payload.email
    password = payload.password
    if Account.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)
    user = Account.objects.create_user(email=email, password=password)
    return JsonResponse({"message": "User created successfully"}, status=201)


def login(request: Request, payload: LoginSchema):
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


def logout(request: Request):
    auth_logout(request)
    LoginLog.objects.create(account=None, ip_address="127.0.0.1", action="logout")
    return JsonResponse({"message": "Logged out successfully"}, status=200)


def request_password_reset(request: Request, payload: PasswordResetRequestSchema):
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
    request: Request, uidb64: str, token: str, payload: PasswordResetSchema
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


def setup_password(request: Request, token: str, payload: PasswordResetSchema):
    password = payload.password
    uid = force_str(urlsafe_base64_decode(token))
    try:
        user = Account.objects.get(pk=uid)
        user.set_password(password)
        user.save()
        return JsonResponse({"message": "Password set successfully"}, status=200)
    except Account.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=400)


def change_password(request: Request, payload: ChangePasswordSchema):
    old_password = payload.old_password
    new_password = payload.new_password
    user = authenticate(username="current_email", password=old_password)
    if user is not None:
        user.set_password(new_password)
        user.save()
        return JsonResponse({"message": "Password changed successfully"}, status=200)
    return JsonResponse({"error": "Invalid credentials"}, status=400)
