from django.conf import settings

class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if not settings.DEBUG:
            # Using wildcards (*.) is the best way to handle Google's multi-domain services
            csp_policy = (
                "default-src 'self'; "
                
                # Allows all Google Translate subdomains (including -pa)
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
                "https://code.jquery.com https://cdn.jsdelivr.net "
                "https://*.googleapis.com https://translate.google.com https://www.gstatic.com; "
                
                # Required for Google Translate's injected styles
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net "
                "https://www.gstatic.com https://fonts.googleapis.com; "
                
                # Allows icons and Google branding
                "img-src 'self' data: https: https://*.gstatic.com https://*.google.com; "
                
                "font-src 'self' data: https://fonts.gstatic.com; "
                
                # Allows the API calls for translations
                "connect-src 'self' https://*.googleapis.com https://translate.google.com "
                "https://*.gstatic.com https://api.emailjs.com; "
                
                "frame-src 'self' https://www.google.com https://translate.google.com; "
                
                "object-src 'none'; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "frame-ancestors 'none'; "
                "upgrade-insecure-requests;"
            )
            response['Content-Security-Policy'] = csp_policy
        
        return response
