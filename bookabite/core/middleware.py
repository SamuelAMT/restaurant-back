import time
import logging
from typing import Callable
from django.http import HttpRequest, HttpResponse
from django.conf import settings

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Middleware to log request details and timing."""
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
        
    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Start timing
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate request duration
        duration = time.time() - start_time
        
        # Log request details
        if settings.DEBUG:
            logger.debug(
                f"[{request.method}] {request.path} "
                f"(Duration: {duration:.2f}s, Status: {response.status_code})"
            )
        
        return response

class SecurityHeadersMiddleware:
    """Middleware to add security headers to responses."""
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
        
    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        
        # Add security headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        if not settings.DEBUG:
            response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

class APIRequestRateLimitMiddleware:
    """Basic rate limiting for API requests."""
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
        self.rate_limit = getattr(settings, 'API_RATE_LIMIT', 100)  # requests per minute
        self.request_logs = {}
        
    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path.startswith('/api/'):
            # Get client IP
            client_ip = request.META.get('HTTP_X_FORWARDED_FOR', 
                                       request.META.get('REMOTE_ADDR'))
            
            # Clean old entries
            current_time = time.time()
            self.request_logs = {
                ip: timestamps for ip, timestamps in self.request_logs.items()
                if current_time - timestamps[-1] < 60
            }
            
            # Check rate limit
            if client_ip in self.request_logs:
                timestamps = self.request_logs[client_ip]
                if len(timestamps) >= self.rate_limit:
                    # Remove timestamps older than 1 minute
                    timestamps = [t for t in timestamps if current_time - t < 60]
                    if len(timestamps) >= self.rate_limit:
                        return HttpResponse(
                            'Rate limit exceeded',
                            status=429
                        )
                
                timestamps.append(current_time)
                self.request_logs[client_ip] = timestamps
            else:
                self.request_logs[client_ip] = [current_time]
        
        return self.get_response(request)