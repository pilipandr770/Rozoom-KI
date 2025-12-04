"""Security headers middleware for Flask application"""
from flask import Flask


def init_security_headers(app: Flask):
    """Initialize security headers for all responses"""
    
    @app.after_request
    def set_security_headers(response):
        """Add security headers to all responses"""
        
        # Strict-Transport-Security (HSTS) - защита от downgrade атак
        # max-age=31536000 (1 год), includeSubDomains, preload
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        # X-Content-Type-Options - защита от MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options - защита от clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Content-Security-Policy (CSP) - защита от XSS и code injection
        # Настроена для работы с inline scripts и styles, которые используются на сайте
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
            "https://cdn.jsdelivr.net "
            "https://unpkg.com "
            "https://cdnjs.cloudflare.com "
            "https://js.stripe.com "
            "https://telegram.org; "
            "style-src 'self' 'unsafe-inline' "
            "https://fonts.googleapis.com "
            "https://cdnjs.cloudflare.com; "
            "font-src 'self' "
            "https://fonts.gstatic.com "
            "data:; "
            "img-src 'self' "
            "data: "
            "https: "
            "blob:; "
            "connect-src 'self' "
            "https://api.openai.com "
            "https://api.stripe.com "
            "wss://; "
            "frame-src 'self' "
            "https://js.stripe.com "
            "https://hooks.stripe.com; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'; "
            "upgrade-insecure-requests;"
        )
        response.headers['Content-Security-Policy'] = csp_policy
        
        # X-XSS-Protection - включает XSS фильтр браузера (legacy, но все еще полезно)
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Permissions-Policy - контроль доступа к API браузера
        permissions_policy = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(self), "
            "usb=(), "
            "interest-cohort=()"  # Защита от FLoC
        )
        response.headers['Permissions-Policy'] = permissions_policy
        
        # Referrer-Policy - контроль передачи referrer
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Удалить заголовок Server (скрыть версию сервера)
        # Cloudflare все равно добавляет свой заголовок Server, но мы можем убрать наш
        response.headers.pop('Server', None)
        
        return response
    
    app.logger.info("✅ Security headers middleware initialized")
