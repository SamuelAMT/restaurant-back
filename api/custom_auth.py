from ninja import Router, Schema
from django.contrib.auth import authenticate, logout as auth_logout
from django.http import HttpRequest
from custom_auth.models import LoginLog
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from custom_auth.authentication import JWTAuth
from custom_auth.serializers import CustomTokenObtainPairSerializer
from custom_auth.views import CustomTokenObtainPairView

auth_router = Router()


class MessageSchema(Schema):
    message: str


class ErrorSchema(Schema):
    detail: str


class LoginSchema(Schema):
    email: str
    password: str


class TokenSchema(Schema):
    access: str
    refresh: str


# Users are being created through the Django admin panel
""" @auth_router.post("/register/")
def register(request, payload):
    return create_user(request, payload) """

# Authenticate user and provide JWT tokens
@auth_router.post("/login/", response={200: TokenSchema, 401: ErrorSchema})
def login(request, payload: LoginSchema):
    email = payload.email
    password = payload.password
    user = authenticate(request, username=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
            "is_admin": user.is_staff,
        }
    else:
        return 401, {"detail": "Invalid credentials"}

@auth_router.post("/token/", response={200: TokenSchema, 401: str})
def obtain_token(request, payload: LoginSchema):
    user = authenticate(request, username=payload.email, password=payload.password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        token = CustomTokenObtainPairSerializer.get_token(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
            "is_admin": user.is_staff,
        }
    return 401, "Invalid credentials"

# Logs out the user session and Creates a logout log entry
@auth_router.post("/logout/", auth=JWTAuth(), response=MessageSchema)
def api_logout(request: HttpRequest):
    # Capture the user before logging out
    user = request.user
    auth_logout(request)
    LoginLog.objects.create(
        custom_user=user,
        ip_address=request.META.get("REMOTE_ADDR", request.META.get('HTTP_X_FORWARDED_FOR', '')),
        action="logout"
    )
    return {"message": "Logged out successfully"}


# Refresh token after expiration
@auth_router.post("/token/refresh/", response={200: TokenSchema, 401: ErrorSchema})
def token_refresh(request, payload: dict):
    response = TokenRefreshView.as_view()(request._request)
    if response.status_code == 200:
        data = response.data
        return data
    else:
        return response.status_code, {"detail": "Token refresh failed"}


# Extracts the refresh token from the Auth header and set Blacklist of expired tokens
@auth_router.post(
    "/logout/expired/", auth=JWTAuth(), response={200: MessageSchema, 400: ErrorSchema}
)
def logout_expired(request: HttpRequest):
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            refresh_token = auth_header.split()[1]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return {"message": "Logout successful"}
        else:
            return 400, {"detail": "Authorization header missing or malformed"}
    except Exception:
        return 400, {"detail": "Invalid token"}


# Manual password reset through `python manage.py changepassword <user>` in terminal
"""
@auth_router.post("/password-reset-request/")
def request_password_reset(request, payload):
    return request_password_reset(request, payload)

@auth_router.post("/password-reset/{uidb64}/{token}/")
def reset_password(request, uidb64, token, payload):
    return reset_password(request, uidb64, token, payload)

@auth_router.post("/setup-password/{token}/")
def setup_password(request, token, payload):
    return setup_password(request, token, payload)

@auth_router.post("/change-password/")
def change_password(request, payload):
    return change_password(request, payload)
"""

# Protected profile endpoint that returns user information.
@auth_router.get("/profile/", auth=JWTAuth(), response={200: Schema, 401: ErrorSchema})
def profile(request: HttpRequest):
    user = request.user
    return {
        "email": user.email,
        "first_name": user.first_name,
    }