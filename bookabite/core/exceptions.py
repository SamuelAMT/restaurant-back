from django.http import JsonResponse
from ninja.errors import HttpError

def custom_exception_handler(request, exc):
    if isinstance(exc, HttpError):
        return JsonResponse(
            {"detail": str(exc)}, 
            status=exc.status_code
        )
    return None