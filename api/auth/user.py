from ninja import Router
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from custom_auth.authentication import JWTAuth
from custom_auth.models import LoginLog, Role
from .schemas import LoginSchema, TokenSchema, ErrorSchema, MessageSchema

user_auth_router = Router()

@user_auth_router.post("/login/", response={200: dict, 401: ErrorSchema})
def user_login(request, payload: LoginSchema):
    user = authenticate(request, username=payload.email, password=payload.password)
    if user is not None and not user.is_superuser:
        refresh = RefreshToken.for_user(user)
        
        LoginLog.objects.create(
            custom_user=user,
            ip_address=request.META.get("REMOTE_ADDR", request.META.get('HTTP_X_FORWARDED_FOR', '')),
            action="login"
        )
        
        restaurant = getattr(user, 'restaurant', None)
        restaurant_data = None
        
        if restaurant:
            restaurant_data = {
                "restaurant_id": str(restaurant.restaurant_id),
                "cnpj": restaurant.cnpj,
                "name": restaurant.name,
                "country_code": restaurant.country_code,
                "phone": restaurant.phone,
                "email": restaurant.email,
                "email_verified": restaurant.email_verified,
                "image": restaurant.image.url if restaurant.image else None,
                "website": restaurant.website,
                "description": restaurant.description,
                "created_at": restaurant.created_at,
                "updated_at": restaurant.updated_at,
                "customers": [str(customer.restaurant_customer_id) for customer in restaurant.customers.all()],
                "employees": [str(employee.restaurant_employee_id) for employee in restaurant.employees.all()],
            }

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
            "is_superuser": user.is_superuser,
            "role": user.role,
            "restaurant": restaurant_data,
        }
    return 401, {"detail": "Invalid credentials"}

@user_auth_router.post("/token/refresh/", response={200: TokenSchema, 401: ErrorSchema})
def token_refresh(request, payload: dict):
    try:
        refresh = RefreshToken(payload.get("refresh"))
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
    except Exception:
        return 401, {"detail": "Invalid refresh token"}

@user_auth_router.post("/logout/", auth=JWTAuth(), response=MessageSchema)
def logout(request):
    try:
        user = request.user
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            refresh_token = auth_header.split()[1]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
        LoginLog.objects.create(
            custom_user=user,
            ip_address=request.META.get("REMOTE_ADDR", request.META.get('HTTP_X_FORWARDED_FOR', '')),
            action="logout"
        )
        return {"message": "Logged out successfully"}
    except Exception:
        return {"message": "Logged out successfully"}