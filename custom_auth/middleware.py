from django.http import JsonResponse
from custom_auth.models import Session
from django.utils import timezone

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_token = request.headers.get('Authorization')

        if session_token:
            try:
                session = Session.objects.get(session_token=session_token)

                if session.expires < timezone.now():
                    return JsonResponse({"error": "Session expired"}, status=401)

                request.user = session.user
            except Session.DoesNotExist:
                return JsonResponse({"error": "Invalid session token"}, status=401)

        return self.get_response(request)
