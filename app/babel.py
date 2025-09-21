from flask import request, g
from flask_babel import Babel, Domain

babel = Babel()

# Определяем дополнительные домены для переводов
payment_domain = Domain(domain='payment_translations')

def get_locale():
    """
    Определяет локаль для текущего запроса.
    
    Приоритет:
    1. Язык из параметра URL (?lang=de)
    2. Язык из cookie
    3. Язык из заголовка Accept-Language
    4. Язык по умолчанию (немецкий)
    """
    # Проверяем параметр URL
    lang = request.args.get('lang')
    if lang in ['en', 'de', 'ru', 'uk']:
        return lang
    
    # Проверяем cookie
    lang = request.cookies.get('lang')
    if lang in ['en', 'de', 'ru', 'uk']:
        return lang
    
    # Проверяем заголовок Accept-Language
    best_match = request.accept_languages.best_match(['en', 'de', 'ru', 'uk'])
    if best_match:
        return best_match
    
    # По умолчанию используем немецкий
    return 'de'

def init_babel(app):
    """Инициализация Flask-Babel"""
    babel.init_app(app, locale_selector=get_locale)
    
    # Регистрируем дополнительные домены
    payment_domain.init_app(app, locale_selector=get_locale)
    
    # Доступ к текущей локали из шаблонов
    @app.before_request
    def before_request():
        g.locale = str(get_locale())
