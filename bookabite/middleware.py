import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from custom_auth.models import BlacklistedToken

class TokenAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = ["/auth/login/", "/auth/register/", "/auth/csrf/"]
        if request.path in excluded_paths:
            return None

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"message": "Authentication token required"}, status=401)

        token = auth_header.split(" ")[1]

        # Check if token is blacklisted
        if BlacklistedToken.objects.filter(token=token).exists():
            return JsonResponse({"message": "Token has been blacklisted"}, status=401)

        try:
            # Decode JWT
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            request.user = user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return JsonResponse({"message": "Invalid or expired token"}, status=403)

        return None
