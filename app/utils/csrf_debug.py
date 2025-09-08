"""
Утилита для проверки работоспособности удаления постов без CSRF защиты.
Используется только для отладки!
"""
from flask import Flask, Blueprint, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect

# Мы будем перехватывать запросы с помощью middleware
class DisableCsrfMiddleware:
    def __init__(self, app, disable_routes):
        self.app = app
        self.disable_routes = disable_routes
        
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        method = environ.get('REQUEST_METHOD', '')
        
        # Проверяем, нужно ли отключить CSRF для этого запроса
        for route in self.disable_routes:
            if path.startswith(route) and method == 'POST':
                environ['SKIP_CSRF_CHECK'] = 'true'
                print(f"[DEBUG] Отключена CSRF защита для {path}")
        
        return self.app(environ, start_response)

def setup_csrf_debugging(app):
    """
    Отключает CSRF защиту для указанных маршрутов.
    Используется только для отладки!
    """
    # Маршруты, для которых нужно отключить CSRF проверку
    disable_routes = [
        '/admin/blog/posts/delete/'  # Маршрут для удаления постов
    ]
    
    # Оборачиваем приложение в middleware
    original_wsgi_app = app.wsgi_app
    app.wsgi_app = DisableCsrfMiddleware(original_wsgi_app, disable_routes)
    
    # Также нужно переопределить метод защиты Flask-WTF
    original_csrf_protect = CSRFProtect._get_csrf_token
    
    def modified_csrf_protect(self):
        if request.environ.get('SKIP_CSRF_CHECK'):
            return True
        return original_csrf_protect(self)
    
    CSRFProtect._get_csrf_token = modified_csrf_protect
    
    app.logger.warning("ВНИМАНИЕ: CSRF защита частично отключена для отладки!")
