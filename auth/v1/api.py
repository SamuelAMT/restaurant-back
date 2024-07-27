from ninja import Router, Form, Schema
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja.security import django_auth

router = Router()

class RegisterSchema(Schema):
    username: str
    email: str
    password1: str
    password2: str

class LoginSchema(Schema):
    username: str
    password: str

class MessageSchema(Schema):
    message: str
    
class ProfileSchema(Schema):
    username: str
    email: str

@router.post("/register", response=MessageSchema)
def register(request: HttpRequest, data: RegisterSchema):
    if data.password1 != data.password2:
        return {"message": "Passwords do not match"}, 400
    
    try:
        user = User.objects.create_user(username=data.username, email=data.email, password=data.password1)
        user.save()
        login(request, user)
        return {"message": "User registered successfully"}, 201
    except Exception as e:
        return {"message": str(e)}, 400

@router.post("/login", response=MessageSchema)
def login_view(request: HttpRequest, data: LoginSchema):
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None:
        login(request, user)
        return {"message": "Successfully logged in"}, 200
    else:
        return {"message": "Invalid credentials"}, 401

@router.post("/logout", response=MessageSchema)
def logout_view(request: HttpRequest):
    logout(request)
    return {"message": "Successfully logged out"}, 200

@router.get("/profile", response=ProfileSchema, auth=django_auth)
def profile_view(request):
    user = request.user
    if user.is_authenticated:
        return {"username": user.username, "email": user.email}
    else:
        return {"message": "User not authenticated"}, 401
