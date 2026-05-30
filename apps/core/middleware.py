import secrets


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Per-request nonce so inline <script> tags can be allowed without
        # opening the door to arbitrary injected scripts ('unsafe-inline').
        nonce = secrets.token_urlsafe(16)
        request.csp_nonce = nonce

        response = self.get_response(request)

        # Content Security Policy.
        # script-src uses a nonce instead of 'unsafe-inline'/'unsafe-eval'.
        # style-src keeps 'unsafe-inline' because inline style="" attributes
        # cannot use a nonce (would require removing every inline style first).
        csp_policies = [
            "default-src 'self'",
            f"script-src 'self' 'nonce-{nonce}'",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "frame-src 'self' https://www.youtube-nocookie.com",
            "img-src 'self' data: https:",
            "connect-src 'self'",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]

        response["Content-Security-Policy"] = "; ".join(csp_policies)
        return response
