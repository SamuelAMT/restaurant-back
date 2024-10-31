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

# Schemas for validation
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

# Testing endpoint
def testing_endpoints(request):
    return render(request, 'auth/testing_endpoints.html')

# Admin account registration
#def create_account(request: HttpRequest, payload: UserCreateSchema):
#    email = payload.email
#    password = payload.password
#    if Account.objects.filter(email=email).exists():
#        return JsonResponse({"error": "Email already exists"}, status=400)
#    admin_account = Account.objects.create_user(email=email, password=password, is_admin=True)
#    return JsonResponse({"message": "Admin account created successfully"}, status=201)

# Main account registration view
def create_account(request, uidb64, token):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.email = email
                user.set_password(password)
                user.is_admin = True
                user.save()
                return JsonResponse({"message": "Admin account created successfully"}, status=201)
            else:
                return JsonResponse({"error": "Invalid or expired link"}, status=400)
        except Account.DoesNotExist:
            return JsonResponse({"error": "Invalid token"}, status=400)
    else:
        return render(request, "custom_auth/register.html", {"uidb64": uidb64, "token": token})

# Send registration link to user
def send_registration_link(email, user_id):
    uid = urlsafe_base64_encode(force_bytes(user_id))
    token = default_token_generator.make_token(user_id)
    registration_url = f"{settings.FRONTEND_URL}/account/register/{uid}/{token}/"
    # Send email logic
    send_mail(
        "Complete your registration",
        f"Please complete your registration by visiting: {registration_url}",
        "no-reply@yourdomain.com",
        [email],
    )

# Custom user registration by admin
def create_user(request: HttpRequest, payload: UserCreateSchema):
    email = payload.email
    password = payload.password
    if Account.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)
    if not request.user.is_authenticated or not request.user.is_admin:
        return JsonResponse({"error": "Only admins can create custom users"}, status=403)
    user = Account.objects.create_user(email=email, password=password, is_admin=False)
    return JsonResponse({"message": "User created successfully"}, status=201)

# Setup password view
def setup_password(request: HttpRequest, token: str, payload: PasswordResetSchema):
    password = payload.password
    uid = force_str(urlsafe_base64_decode(request.GET.get("uid")))
    try:
        user = Account.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return JsonResponse({"message": "Password set successfully"}, status=200)
        else:
            return JsonResponse({"error": "Invalid or expired token"}, status=400)
    except Account.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


# Login view
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

# Logout view
def logout(request: HttpRequest):
    auth_logout(request)
    LoginLog.objects.create(account=None, ip_address="127.0.0.1", action="logout")
    return JsonResponse({"message": "Logged out successfully"}, status=200)

# Password reset request
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

# Reset password view
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

# Change password view
def change_password(request: HttpRequest, payload: ChangePasswordSchema):
    old_password = payload.old_password
    new_password = payload.new_password
    user = authenticate(username=request.user.email, password=old_password)
    if user is not None:
        user.set_password(new_password)
        user.save()
        return JsonResponse({"message": "Password changed successfully"}, status=200)
    return JsonResponse({"error": "Invalid credentials"}, status=400)

# Views for login, logout, and password reset using Django views
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
