from ninja import Router
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .schemas import LoginSchema, ErrorSchema
from custom_auth.models import LoginLog

admin_auth_router = Router()

@admin_auth_router.post("/login/", response={200: dict, 401: ErrorSchema})
def admin_login(request, payload: LoginSchema):
    """
    API endpoint for superuser authentication.
    This is separate from Django's built-in admin interface.
    """
    user = authenticate(request, username=payload.email, password=payload.password)
    if user is not None and user.is_superuser:
        refresh = RefreshToken.for_user(user)
        
        LoginLog.objects.create(
            custom_user=user,
            ip_address=request.META.get("REMOTE_ADDR", request.META.get('HTTP_X_FORWARDED_FOR', '')),
            action="login"
        )
        
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
            "is_superuser": user.is_superuser
        }
    return 401, {"detail": "Invalid credentials or insufficient permissions"}