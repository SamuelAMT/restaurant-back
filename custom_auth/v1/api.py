from ninja import Router, Form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest
from django.utils.timezone import now
from datetime import timedelta
import jwt
from django.conf import settings
from ninja.errors import HttpError
from ninja.security import HttpBearer
from ..models import LoginLog, BlacklistedToken
from .schemas import (
    RegisterSchema,
    LoginSchema,
    TokenSchema,
    MessageSchema,
    ProfileSchema,
)

router = Router()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            if not user.is_active:
                raise HttpError(403, "User is not active")
            if BlacklistedToken.objects.filter(token=token).exists():
                raise HttpError(403, "Token has been blacklisted")
            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            raise HttpError(403, "Invalid token")


def create_jwt_token(user, token_type="access", expiration_days=90):
    exp_time = now() + timedelta(days=expiration_days)
    payload = {
        "user_id": user.id,
        "exp": exp_time,
        "iat": now(),
        "type": token_type,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


@router.post("/register", response=MessageSchema)
def register(request: HttpRequest, data: RegisterSchema):
    if data.password1 != data.password2:
        return {"message": "Passwords do not match"}, 400

    try:
        user = User.objects.create_user(
            username=data.username, email=data.email, password=data.password1
        )
        user.save()
        login(request, user)
        return {"message": "User registered successfully"}, 201
    except Exception as e:
        return {"message": str(e)}, 400


@router.post("/login", response={200: TokenSchema, 401: MessageSchema})
def login_view(request: HttpRequest, data: LoginSchema):
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None:
        login(request, user)
        access_token = create_jwt_token(user, token_type="access", expiration_days=90)
        refresh_token = create_jwt_token(user, token_type="refresh", expiration_days=90)
        LoginLog.objects.create(
            user=user,
            login_time=now(),
            method="standard",
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )
        return {"access": access_token, "refresh": refresh_token}, 200
    else:
        return {"message": "Invalid credentials"}, 401


@router.post("/logout", response=MessageSchema, auth=AuthBearer())
def logout_view(request: HttpRequest):
    user = request.user
    token = request.META.get("HTTP_AUTHORIZATION").split()[1]
    BlacklistedToken.objects.create(token=token)
    logout(request)
    return {"message": "Successfully logged out"}, 200


@router.get("/profile", response=ProfileSchema, auth=AuthBearer())
def profile_view(request):
    user = request.auth
    return {"username": user.username, "email": user.email}
