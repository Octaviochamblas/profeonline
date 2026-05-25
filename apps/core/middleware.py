class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Gradual Content Security Policy allowing local assets, Google Fonts, and YouTube embeds
        csp_policies = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "frame-src 'self' https://www.youtube-nocookie.com",
            "img-src 'self' data: https:",
            "connect-src 'self'",
        ]
        
        response["Content-Security-Policy"] = "; ".join(csp_policies)
        return response
