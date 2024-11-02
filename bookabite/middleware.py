""" import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from custom_auth.models import Account, BlacklistedToken

class TokenAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = [
            "/auth/login/", 
            "/auth/register/", 
            "/auth/csrf/",
            "/auth/password-reset/",
            "/auth/password-reset-confirm/",
            "/custom_auth/templates/custom_auth/testing_endpoints.html",
            "/account/register/",
        ]
        
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
            user = Account.objects.get(id=payload["user_id"])  # Using Account model
            request.user = user
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Token has expired"}, status=403)
        except jwt.InvalidTokenError:
            return JsonResponse({"message": "Invalid token"}, status=403)
        except Account.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=403)

        return None
 """