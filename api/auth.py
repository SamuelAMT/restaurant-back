from ninja import Router, Form, Schema
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from ninja.security import django_auth

router = Router()

class LoginSchema(Schema):
    username: str
    password: str

class MessageSchema(Schema):
    message: str
    
class ProfileSchema(Schema):
    username: str
    email: str

@router.post("/login", response=MessageSchema)
def login_view(request: HttpRequest, data: LoginSchema = Form(...)):
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None:
        login(request, user)
        return {"message": "Successfully logged in"}
    else:
        return {"message": "Invalid credentials"}, 401

@router.post("/logout", response=MessageSchema)
def logout_view(request: HttpRequest):
    logout(request)
    return {"message": "Successfully logged out"}

@router.get("/profile", response=ProfileSchema, auth=django_auth)
def profile_view(request):
    user = request.user
    if user.is_authenticated:
        return {"username": user.username, "email": user.email}
    else:
        return {"message": "User not authenticated"}, 401
