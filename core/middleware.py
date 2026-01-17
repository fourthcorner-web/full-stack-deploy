"""
Custom middleware for Content Security Policy (CSP) headers
"""
from django.conf import settings


class CSPMiddleware:
    """
    Middleware to add Content Security Policy headers
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only add CSP in production or when explicitly enabled
        if not settings.DEBUG:
            # Basic CSP policy - adjust as needed for your application
            csp_policy = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://code.jquery.com https://cdn.jsdelivr.net https://translate.google.com https://translate.googleapis.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self' https://translate.google.com https://translate.googleapis.com https://api.emailjs.com; "
                "frame-src 'self' https://www.google.com https://maps.google.com https://translate.google.com; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "frame-ancestors 'none'; "
                "upgrade-insecure-requests;"
            )
            response['Content-Security-Policy'] = csp_policy
        
        return response
