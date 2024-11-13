from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger(__name__)

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            request.user = user
            return user
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return None